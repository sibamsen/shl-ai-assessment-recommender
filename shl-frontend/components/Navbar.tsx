import { BrainCircuit } from "lucide-react";

export default function Navbar() {
  return (
    <nav
      className="
      sticky
      top-0
      z-50
      backdrop-blur-xl
      border-b
      border-slate-800
      bg-[#0B1120]/70
      "
    >
      <div className="max-w-7xl mx-auto flex items-center justify-between px-8 py-5">

        <div className="flex items-center gap-3">

          <BrainCircuit
            size={30}
            className="text-blue-500"
          />

          <h1 className="text-2xl font-bold">
            SHL AI
          </h1>

        </div>

        <div className="space-x-8 text-sm font-medium">

          <a
            href="/"
            className="hover:text-blue-400 transition"
          >
            Home
          </a>

          <a
            href="https://shl-ai-assessment-recommender-production-c834.up.railway.app/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-blue-400 transition"
          >
            API Docs
          </a>

          <a
            href="https://github.com/sibamsen/shl-ai-assessment-recommender"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-blue-400 transition"
          >
            GitHub
          </a>

        </div>

      </div>

    </nav>
  );
}