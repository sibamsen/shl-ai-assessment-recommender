"use client";

import { useState, useEffect, useRef } from "react";
import { Search } from "lucide-react";
import { Oval } from "react-loader-spinner";

import { api } from "@/lib/api";
import RecommendationCard from "./RecommendationCard";
import ChatMessage from "./ChatMessage";

interface Recommendation {
  name: string;
  url: string;
  test_type: string;
  duration: string;
  languages: string[];
  keys: string[];
}

interface ChatMessageType {
  role: "user" | "assistant";
  content: string;
}

export default function SearchBox() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState<ChatMessageType[]>([]);

  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);

  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, recommendations]);

  const handleSearch = async () => {
    if (!query.trim()) {
      alert("Please enter your hiring requirement.");
      return;
    }

    setLoading(true);

    // Clear previous recommendation cards
    setRecommendations([]);

    try {
      const response = await api.post("/chat", {
        messages: [
          ...messages,
          {
            role: "user",
            content: query,
          },
        ],
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "user",
          content: query,
        },
        {
          role: "assistant",
          content: response.data.reply,
        },
      ]);

      setRecommendations(response.data.recommendations);

      setQuery("");
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "⚠ Unable to connect to the backend. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-6 pb-20">

      <div className="bg-[#111827] rounded-3xl border border-slate-700 p-6 shadow-2xl">

        <textarea
          rows={4}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Example: I need assessments for hiring graduate software engineers..."
          className="w-full bg-transparent outline-none resize-none text-lg text-white placeholder:text-slate-500"
        />

        <div className="flex justify-end mt-6">

          <button
            onClick={handleSearch}
            disabled={loading}
            className="flex items-center gap-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-60 px-7 py-3 rounded-xl font-semibold transition-all"
          >
            {loading ? (
              <Oval
                height={22}
                width={22}
                color="white"
                secondaryColor="#60A5FA"
                strokeWidth={5}
              />
            ) : (
              <>
                <Search size={18} />
                ✨ Find Assessments
              </>
            )}
          </button>

        </div>

      </div>

      {/* Welcome Message */}
      {!loading && messages.length === 0 && (
        <div className="mt-12">
          <ChatMessage
            role="assistant"
            message="👋 Hello! I'm your SHL AI Assistant. Describe the role you're hiring for, and I'll recommend the most relevant SHL assessments."
          />
        </div>
      )}

      {/* Conversation */}
      {messages.length > 0 && (
        <div className="mt-10 space-y-6">
          {messages.map((message, index) => (
            <ChatMessage
              key={index}
              role={message.role}
              message={message.content}
            />
          ))}
        </div>
      )}

      {/* Loading Assistant */}
      {loading && (
        <div className="mt-6">
          <ChatMessage
            role="assistant"
            message="🔍 Searching the SHL catalog and preparing recommendations..."
          />
        </div>
      )}

      {/* Recommendation Cards */}
      {recommendations.length > 0 && (
        <div className="grid md:grid-cols-2 gap-7 mt-10">
          {recommendations.map((item) => (
            <RecommendationCard
              key={item.name}
              name={item.name}
              type={item.test_type}
              url={item.url}
              duration={item.duration}
              languages={item.languages}
              keys={item.keys}
            />
          ))}
        </div>
      )}

      <div ref={bottomRef} />

    </div>
  );
}