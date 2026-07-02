from pathlib import Path


def repair_multiline_strings(input_path: Path, output_path: Path):
    """
    Repairs malformed JSON files where string values
    are accidentally split across multiple lines.
    """

    repaired_lines = []

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    i = 0

    while i < len(lines):

        line = lines[i]

        # Detect a line that starts a string but does not close it
        if (
            '": "' in line
            and line.count('"') % 2 != 0
        ):

            merged = line.rstrip("\n")

            i += 1

            while i < len(lines):

                merged += " " + lines[i].strip()

                # Stop when closing quote appears
                if '"' in lines[i]:
                    break

                i += 1

            repaired_lines.append(merged + "\n")

        else:
            repaired_lines.append(line)

        i += 1

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(repaired_lines)