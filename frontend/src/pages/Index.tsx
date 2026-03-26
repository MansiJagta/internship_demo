import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Search, Sparkles, Bot, Shield, TrendingUp, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useQuery, useMutation } from "@tanstack/react-query";
import { fetchVehicles, semanticSearch } from "@/lib/api";
import VehicleCard from "@/components/VehicleCard";
import SkeletonCard from "@/components/SkeletonCard";

export default function Index() {
  const navigate = useNavigate();
  const [searchMode, setSearchMode] = useState<"standard" | "vibe">("standard");
  const [query, setQuery] = useState("");

  const { data: featured, isLoading } = useQuery({
    queryKey: ["featured-vehicles"],
    queryFn: () => fetchVehicles(),
    select: data => data.slice(0, 4),
  });

  const vibeMutation = useMutation({
    mutationFn: semanticSearch,
    onSuccess: () => navigate("/browse"),
  });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchMode === "vibe" && query) {
      vibeMutation.mutate(query);
    } else {
      navigate(`/browse?q=${encodeURIComponent(query)}`);
    }
  };

  const steps = [
    { icon: Search, title: "Search with Vibes", desc: "Describe your dream car in natural language — our AI understands intent, not just keywords." },
    { icon: Shield, title: "AI Anomaly Detection", desc: "Every listing is scanned for pricing inconsistencies and suspicious patterns." },
    { icon: Bot, title: "Negotiate with AI", desc: "Our agentic negotiator handles price discussions on your behalf, 24/7." },
    { icon: TrendingUp, title: "Close the Deal", desc: "Track all your offers in one dashboard. Accept, counter, or walk away." },
  ];

  return (
    <>
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-primary/5 via-transparent to-transparent" />
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full bg-primary/5 blur-[120px]" />

        <div className="container relative pt-24 pb-20 md:pt-32 md:pb-28">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="max-w-3xl mx-auto text-center space-y-6"
          >
            <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight">
              Find Your Perfect Ride with{" "}
              <span className="text-gradient">AI-Powered</span> Search
            </h1>
            <p className="text-lg text-muted-foreground max-w-xl mx-auto">
              AutoVibe uses semantic search and agentic negotiation to transform how you buy and sell vehicles.
            </p>

            {/* Dual Search Bar */}
            <form onSubmit={handleSearch} className="glass glow-primary rounded-2xl p-2 max-w-2xl mx-auto">
              <div className="flex gap-1 mb-2 bg-muted/30 rounded-xl p-1">
                <button
                  type="button"
                  onClick={() => setSearchMode("standard")}
                  className={`flex-1 py-2 rounded-lg text-sm font-medium transition-all ${
                    searchMode === "standard" ? "bg-card text-foreground shadow-sm" : "text-muted-foreground"
                  }`}
                >
                  <Search className="w-3.5 h-3.5 inline mr-1.5" />
                  Standard
                </button>
                <button
                  type="button"
                  onClick={() => setSearchMode("vibe")}
                  className={`flex-1 py-2 rounded-lg text-sm font-medium transition-all ${
                    searchMode === "vibe" ? "bg-primary/20 text-primary shadow-sm" : "text-muted-foreground"
                  }`}
                >
                  <Sparkles className="w-3.5 h-3.5 inline mr-1.5" />
                  Vibe Search
                </button>
              </div>

              <div className="flex gap-2">
                <input
                  value={query}
                  onChange={e => setQuery(e.target.value)}
                  placeholder={searchMode === "vibe"
                    ? "A fast electric car under $100k with a futuristic vibe..."
                    : "Search by make, model, or keyword..."
                  }
                  className="flex-1 bg-transparent px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none"
                />
                <Button type="submit" disabled={vibeMutation.isPending} className="px-6">
                  {vibeMutation.isPending ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    "Search"
                  )}
                </Button>
              </div>

              {vibeMutation.isPending && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex items-center gap-2 px-4 py-2 text-sm text-primary"
                >
                  <Sparkles className="w-4 h-4 animate-pulse" />
                  AI is thinking — running semantic vector search...
                </motion.div>
              )}
            </form>
          </motion.div>
        </div>
      </section>

      {/* How it Works */}
      <section className="container py-20">
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl font-bold">How AutoVibe Works</h2>
          <p className="text-muted-foreground mt-2">AI-powered from search to close</p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {steps.map((step, i) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="glass rounded-xl p-6 text-center space-y-3 glass-hover"
            >
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mx-auto">
                <step.icon className="w-6 h-6 text-primary" />
              </div>
              <h3 className="font-semibold">{step.title}</h3>
              <p className="text-sm text-muted-foreground">{step.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Featured */}
      <section className="container pb-20">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-2xl font-bold">Featured Listings</h2>
          <Button variant="outline" onClick={() => navigate("/browse")}>View All</Button>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {isLoading
            ? Array.from({ length: 4 }).map((_, i) => <SkeletonCard key={i} />)
            : featured?.map((v, i) => <VehicleCard key={v.id} vehicle={v} index={i} />)
          }
        </div>
      </section>
    </>
  );
}
