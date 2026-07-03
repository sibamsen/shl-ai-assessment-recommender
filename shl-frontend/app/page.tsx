import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import SearchBox from "@/components/SearchBox";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <main
      className="
        min-h-screen
        bg-gradient-to-br
        from-[#020617]
        via-[#0F172A]
        to-[#111827]
        text-white
      "
    >
      <Navbar />
      <Hero />
      <SearchBox />
      <Footer />
    </main>
  );
}
