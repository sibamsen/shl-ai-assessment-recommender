export default function Hero() {
  return (
    <section className="relative overflow-hidden">

      <div className="absolute inset-0 bg-gradient-to-br from-blue-900/30 via-transparent to-cyan-500/10 blur-3xl" />

      <div className="relative py-24 text-center">

        <p className="uppercase tracking-[0.3em] text-blue-400 text-sm">

          AI Powered Recruitment

        </p>

        <h1 className="mt-5 text-6xl font-black">

          Find the Perfect

          <span className="text-blue-500">

            {" "}SHL Assessment

          </span>

        </h1>

        <p className="mt-8 text-xl text-slate-400 max-w-3xl mx-auto">

          Instantly discover the best SHL assessments using AI,
          semantic search and intelligent recommendation.

        </p>

      </div>

    </section>
  );
}