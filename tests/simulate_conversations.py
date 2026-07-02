import os
import re
import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Any

# Ensure project root is on path and .env is loaded before any app imports
PROJECT_ROOT = Path("C:/Users/Dell/Desktop/DATA ANALYTICS/Projects/SHL_AI_Recommender")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from app.conversation.manager import ConversationManager

# Normalize strings for comparison
def normalize_name(s: str) -> str:
    s = s.lower()
    s = s.replace("\u2013", "-").replace("\u2014", "-")
    s = re.sub(r'[^a-z0-9]', '', s)
    return s


def parse_trace_file(path: Path) -> List[Dict[str, Any]]:
    content = path.read_text(encoding="utf-8")
    turns = []

    # Split content by turns
    turn_blocks = re.split(r'### Turn \d+', content)
    # The first block is header/metadata, ignore it
    for block in turn_blocks[1:]:
        lines = block.splitlines()

        user_msg = ""
        expected_recs = []
        is_end = False

        # Parse user message (lines starting with ">")
        user_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(">"):
                user_lines.append(stripped.lstrip(">").strip())
        user_msg = " ".join(user_lines).strip()

        # Parse expected recommendations from table rows like: | 1 | Name | ... |
        table_rows = re.findall(r'\|\s*\d+\s*\|\s*([^|]+)\s*\|', block)
        for row in table_rows:
            name = row.strip().replace("**", "").strip()
            # Skip header row
            if name.lower() in ("name", "") or name.startswith("---"):
                continue
            expected_recs.append(name)

        # Parse end_of_conversation flag
        if "end_of_conversation" in block.lower():
            end_match = re.search(r'end_of_conversation[`\s]*:?\s*\*?\*?([Tt]rue|[Ff]alse)\*?\*?', block)
            if end_match:
                is_end = end_match.group(1).lower() == "true"

        turns.append({
            "user": user_msg,
            "expected_recs": expected_recs,
            "end_of_conversation": is_end
        })

    return turns


def call_with_retry(manager: ConversationManager, history: List[Dict], max_retries: int = 5) -> Dict:
    """Call process_chat with exponential backoff on rate-limit errors."""
    for attempt in range(max_retries):
        try:
            return manager.process_chat(history)
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "ResourceExhausted" in err_str or "quota" in err_str.lower():
                # Extract suggested retry delay if present
                delay_match = re.search(r'retry in (\d+)', err_str)
                wait = int(delay_match.group(1)) + 5 if delay_match else (2 ** attempt) * 10
                print(f"  [Rate limit] Waiting {wait}s before retry (attempt {attempt+1}/{max_retries})...")
                time.sleep(wait)
            else:
                # Non-retriable error — re-raise
                raise
    raise RuntimeError(f"Max retries ({max_retries}) exceeded due to rate limits.")


def run_simulation():
    print("=" * 60)
    print("SHL Recommender Conversation Trace Replay & Evals")
    print("=" * 60)

    catalog_path = PROJECT_ROOT / "data/processed/shl_product_catalog_clean.json"
    traces_dir = Path("C:/Users/Dell/Desktop/DATA ANALYTICS/Projects/sample_conversations/GenAI_SampleConversations")

    if not catalog_path.exists():
        print("Error: Cleaned catalog not found. Run clean_catalog.py first.")
        return

    # Initialize manager once
    manager = ConversationManager(catalog_path)

    total_traces = 0
    passed_traces = 0
    all_recalls = []

    trace_files = sorted(
        traces_dir.glob("*.md"),
        key=lambda p: int(re.search(r'\d+', p.name).group())
    )

    for trace_path in trace_files:
        print(f"\nReplaying Trace: {trace_path.name}")
        print("-" * 40)

        turns = parse_trace_file(trace_path)
        history = []
        trace_recalls = []

        for idx, turn in enumerate(turns, 1):
            user_text = turn["user"]
            expected = turn["expected_recs"]
            expected_end = turn["end_of_conversation"]

            if not user_text:
                print(f"Turn {idx} | (empty user message, skipping)")
                continue

            print(f"Turn {idx} | User: {user_text[:70]}...")

            # Append user message
            history.append({"role": "user", "content": user_text})

            # Call agent with retry
            response = call_with_retry(manager, history)

            reply = response["reply"]
            recs = response["recommendations"]
            end_conv = response["end_of_conversation"]

            # Append assistant message (without table for cleaner history)
            table_idx = reply.find("\n\n| # | Name |")
            clean_reply = reply[:table_idx].strip() if table_idx != -1 else reply
            history.append({"role": "assistant", "content": clean_reply})

            # Evaluate Turn
            rec_names = [r["name"] for r in recs]

            # Calculate Recall
            if expected:
                matched = 0
                for exp_name in expected:
                    norm_exp = normalize_name(exp_name)
                    if any(
                        normalize_name(r) == norm_exp
                        or norm_exp in normalize_name(r)
                        or normalize_name(r) in norm_exp
                        for r in rec_names
                    ):
                        matched += 1
                recall = matched / len(expected)
                trace_recalls.append(recall)
                status = "OK" if recall >= 1.0 else "PARTIAL" if recall > 0 else "MISS"
                print(f"  [{status}] Expected: {len(expected)} | Got: {len(rec_names)} | Recall: {recall:.2f}")
                if recall < 1.0:
                    missing = [e for e in expected if not any(
                        normalize_name(e) in normalize_name(r) or normalize_name(r) in normalize_name(e)
                        for r in rec_names
                    )]
                    print(f"  Missing: {missing}")
            else:
                # Expect empty recs this turn
                if rec_names:
                    print(f"  [WARN] Expected NO recs, got: {rec_names[:3]}{'...' if len(rec_names)>3 else ''}")
                    trace_recalls.append(0.0)
                else:
                    print("  [OK] No recs returned (as expected).")
                    trace_recalls.append(1.0)

            # Check end of conversation flag on last turn
            if idx == len(turns):
                flag_ok = end_conv == expected_end
                print(f"  end_of_conversation: got={end_conv}, expected={expected_end} {'OK' if flag_ok else 'MISMATCH'}")

            # Small inter-turn delay to stay under rate limits
            time.sleep(3)

        # Average recall for this trace
        avg_recall = sum(trace_recalls) / len(trace_recalls) if trace_recalls else 1.0
        all_recalls.append(avg_recall)
        print(f"Finished {trace_path.name} | Avg Trace Recall: {avg_recall:.2f}")

        total_traces += 1
        if avg_recall >= 0.85:
            passed_traces += 1

        # Inter-trace delay to avoid rate limit carryover
        time.sleep(10)

    mean_recall = sum(all_recalls) / len(all_recalls) if all_recalls else 0.0
    print("\n" + "=" * 60)
    print("FINAL EVALUATION METRICS")
    print("=" * 60)
    print(f"Total Traces Replayed  : {total_traces}")
    print(f"Passed (>=85% Recall)  : {passed_traces} / {total_traces}")
    print(f"Mean Recall@10         : {mean_recall:.2%}")
    print(f"Per-trace recalls      : {[round(r, 2) for r in all_recalls]}")
    print("=" * 60)


if __name__ == "__main__":
    run_simulation()
