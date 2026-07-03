import {
  ExternalLink,
  Brain,
  BadgeCheck,
  Clock3,
  Globe,
  Target,
} from "lucide-react";

import { motion } from "framer-motion";

type Props = {
  name: string;
  type: string;
  url: string;
  duration: string;
  languages: string[];
  keys: string[];
};

export default function RecommendationCard({
  name,
  type,
  url,
  duration,
  languages,
  keys,
}: Props) {
  const assessmentType =
    type === "K"
      ? "Knowledge & Skills"
      : type === "A"
      ? "Ability & Aptitude"
      : type;

  return (
    <motion.div
      initial={{ opacity: 0, y: 25 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35 }}
      whileHover={{
        scale: 1.02,
        transition: { duration: 0.2 },
      }}
      className="
      group
      rounded-3xl
      border
      border-slate-700
      bg-gradient-to-br
      from-slate-900
      via-slate-800
      to-slate-900
      p-7
      shadow-lg
      transition-all
      duration-300
      hover:border-blue-500
      hover:shadow-2xl
      hover:shadow-blue-900/40
      "
    >
      {/* Header */}

      <div className="flex items-center gap-4">

        <div
          className="
          bg-blue-600
          p-3
          rounded-xl
          group-hover:rotate-6
          transition-transform
          "
        >
          <Brain size={24} />
        </div>

        <div>

          <h2 className="text-xl font-bold text-white">

            {name}

          </h2>

          <p className="text-slate-400 text-sm">

            SHL Assessment

          </p>

        </div>

      </div>

      {/* Assessment Type */}

      <div className="mt-6">

        <span
          className="
          inline-flex
          items-center
          gap-2
          rounded-full
          bg-blue-900/30
          border
          border-blue-500
          px-4
          py-2
          text-sm
          text-blue-200
          "
        >

          <BadgeCheck size={16} />

          {assessmentType}

        </span>

      </div>

      {/* Duration */}

      <div className="mt-7 flex items-center gap-3 text-slate-300">

        <Clock3
          size={18}
          className="text-blue-400"
        />

        <span>

          {duration || "Not specified"}

        </span>

      </div>

      {/* Languages */}

      <div className="mt-6">

        <div className="flex items-center gap-3 mb-3">

          <Globe
            size={18}
            className="text-blue-400"
          />

          <span className="font-medium">

            Languages

          </span>

        </div>

        <div className="flex flex-wrap gap-2">

          {(languages ?? []).slice(0, 4).map((lang) => (

            <span
              key={lang}
              className="
              rounded-full
              bg-slate-700
              px-3
              py-1
              text-xs
              "
            >
              {lang}
            </span>

          ))}

        </div>

      </div>

      {/* Competencies */}

      <div className="mt-6">

        <div className="flex items-center gap-3 mb-3">

          <Target
            size={18}
            className="text-blue-400"
          />

          <span className="font-medium">

            Competencies

          </span>

        </div>

        <div className="flex flex-wrap gap-2">

          {(keys ?? []).map((key) => (

            <span
              key={key}
              className="
              rounded-full
              bg-blue-950
              border
              border-blue-700
              px-3
              py-1
              text-xs
              text-blue-200
              "
            >
              {key}
            </span>

          ))}

        </div>

      </div>

      {/* Button */}

      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        className="
        mt-8
        flex
        items-center
        justify-center
        gap-2
        rounded-xl
        bg-blue-600
        py-3
        font-semibold
        transition-all
        hover:bg-blue-700
        hover:scale-[1.02]
        "
      >

        View Assessment

        <ExternalLink size={18} />

      </a>

    </motion.div>
  );
}