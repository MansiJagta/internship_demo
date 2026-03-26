import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { SlidersHorizontal, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { fetchVehicles } from "@/lib/api";
import VehicleCard from "@/components/VehicleCard";
import SkeletonCard from "@/components/SkeletonCard";

const makes = ["All", "Tesla", "BMW", "Porsche", "Mercedes-Benz", "Audi", "Lamborghini", "Ford", "Rivian"];

export default function Browse() {
  const [filtersOpen, setFiltersOpen] = useState(false);
  const [make, setMake] = useState("All");
  const [priceRange, setPriceRange] = useState([0, 300000]);
  const [yearRange, setYearRange] = useState([2020, 2025]);
  const [maxMileage, setMaxMileage] = useState(100000);

  const { data: vehicles, isLoading } = useQuery({
    queryKey: ["vehicles", make, priceRange, yearRange, maxMileage],
    queryFn: () => fetchVehicles({
      make: make === "All" ? undefined : make,
      min_price: priceRange[0], max_price: priceRange[1],
      min_year: yearRange[0], max_year: yearRange[1],
      max_mileage: maxMileage,
    }),
  });

  const FilterContent = () => (
    <div className="space-y-6">
      <div>
        <h4 className="text-sm font-semibold mb-3">Make</h4>
        <div className="flex flex-wrap gap-2">
          {makes.map(m => (
            <button
              key={m}
              onClick={() => setMake(m)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                make === m ? "bg-primary text-primary-foreground" : "bg-muted/50 text-muted-foreground hover:text-foreground"
              }`}
            >
              {m}
            </button>
          ))}
        </div>
      </div>

      <div>
        <div className="flex justify-between text-sm mb-3">
          <span className="font-semibold">Price Range</span>
          <span className="text-muted-foreground">${priceRange[0].toLocaleString()} – ${priceRange[1].toLocaleString()}</span>
        </div>
        <Slider value={priceRange} onValueChange={setPriceRange} min={0} max={300000} step={5000} />
      </div>

      <div>
        <div className="flex justify-between text-sm mb-3">
          <span className="font-semibold">Year</span>
          <span className="text-muted-foreground">{yearRange[0]} – {yearRange[1]}</span>
        </div>
        <Slider value={yearRange} onValueChange={setYearRange} min={2015} max={2025} step={1} />
      </div>

      <div>
        <div className="flex justify-between text-sm mb-3">
          <span className="font-semibold">Max Mileage</span>
          <span className="text-muted-foreground">{maxMileage.toLocaleString()} mi</span>
        </div>
        <Slider value={[maxMileage]} onValueChange={([v]) => setMaxMileage(v)} min={0} max={200000} step={5000} />
      </div>
    </div>
  );

  return (
    <div className="container py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Browse Vehicles</h1>
        <Button variant="outline" size="sm" className="lg:hidden" onClick={() => setFiltersOpen(!filtersOpen)}>
          <SlidersHorizontal className="w-4 h-4 mr-2" />
          Filters
        </Button>
      </div>

      <div className="flex gap-8">
        {/* Desktop sidebar */}
        <aside className="hidden lg:block w-72 shrink-0">
          <div className="glass rounded-xl p-6 sticky top-24">
            <h3 className="font-semibold mb-4">Filters</h3>
            <FilterContent />
          </div>
        </aside>

        {/* Mobile filter drawer */}
        {filtersOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="fixed inset-0 z-40 lg:hidden"
          >
            <div className="absolute inset-0 bg-background/80 backdrop-blur-sm" onClick={() => setFiltersOpen(false)} />
            <motion.div
              initial={{ y: "100%" }}
              animate={{ y: 0 }}
              className="absolute bottom-0 left-0 right-0 glass rounded-t-2xl p-6 max-h-[80vh] overflow-y-auto"
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold">Filters</h3>
                <button onClick={() => setFiltersOpen(false)}>
                  <X className="w-5 h-5 text-muted-foreground" />
                </button>
              </div>
              <FilterContent />
            </motion.div>
          </motion.div>
        )}

        {/* Vehicle grid */}
        <div className="flex-1">
          <p className="text-sm text-muted-foreground mb-4">
            {isLoading ? "Loading..." : `${vehicles?.length ?? 0} vehicles found`}
          </p>
          <div className="grid sm:grid-cols-2 xl:grid-cols-3 gap-6">
            {isLoading
              ? Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)
              : vehicles?.map((v, i) => <VehicleCard key={v.id} vehicle={v} index={i} />)
            }
          </div>
          {!isLoading && vehicles?.length === 0 && (
            <div className="text-center py-20 text-muted-foreground">
              No vehicles match your filters. Try adjusting your criteria.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
