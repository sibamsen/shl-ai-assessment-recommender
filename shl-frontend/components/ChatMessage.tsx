type Props = {
  role: "user" | "assistant";
  message: string;
};

export default function ChatMessage({
  role,
  message,
}: Props) {
  const isUser = role === "user";

  return (
    <div
      className={`flex ${
        isUser ? "justify-end" : "justify-start"
      } mb-6`}
    >
      <div
        className={`max-w-3xl rounded-3xl px-6 py-4 whitespace-pre-wrap leading-8 ${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-[#111827] border border-slate-700 text-slate-300"
        }`}
      >
        {message}
      </div>
    </div>
  );
}