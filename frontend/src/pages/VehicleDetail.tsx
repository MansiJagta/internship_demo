import { useState } from "react";
import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import {
  ArrowLeft, MapPin, Calendar, Gauge, Fuel, Cog, Zap, Palette,
  ShieldAlert, AlertTriangle, Sparkles, MessageSquare, ChevronLeft, ChevronRight,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { fetchVehicle } from "@/lib/api";
import NegotiationPanel from "@/components/NegotiationPanel";

export default function VehicleDetail() {
  const { id } = useParams<{ id: string }>();
  const [selectedImg, setSelectedImg] = useState(0);
  const [negoOpen, setNegoOpen] = useState(false);

  const { data: vehicle, isLoading } = useQuery({
    queryKey: ["vehicle", id],
    queryFn: () => fetchVehicle(id!),
    enabled: !!id,
  });

  if (isLoading) {
    return (
      <div className="container py-8 space-y-6">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="aspect-[16/9] w-full rounded-xl" />
        <div className="grid md:grid-cols-2 gap-6">
          <Skeleton className="h-64 rounded-xl" />
          <Skeleton className="h-64 rounded-xl" />
        </div>
      </div>
    );
  }

  if (!vehicle) {
    return (
      <div className="container py-20 text-center">
        <h2 className="text-2xl font-bold mb-2">Vehicle Not Found</h2>
        <Link to="/browse" className="text-primary hover:underline">Back to browse</Link>
      </div>
    );
  }

  const specs = [
    { icon: Calendar, label: "Year", value: vehicle.year },
    { icon: Gauge, label: "Mileage", value: `${vehicle.mileage.toLocaleString()} mi` },
    { icon: Fuel, label: "Fuel", value: vehicle.fuel_type },
    { icon: Cog, label: "Transmission", value: vehicle.transmission },
    { icon: Zap, label: "Horsepower", value: `${vehicle.horsepower} hp` },
    { icon: Cog, label: "Drivetrain", value: vehicle.drivetrain },
    { icon: Palette, label: "Exterior", value: vehicle.exterior_color },
    { icon: Palette, label: "Interior", value: vehicle.interior_color },
  ];

  const title = `${vehicle.year} ${vehicle.make} ${vehicle.model}`;

  return (
    <>
      <div className="container py-8 max-w-6xl">
        <Link to="/browse" className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground mb-6">
          <ArrowLeft className="w-4 h-4" /> Back to listings
        </Link>

        <div className="grid lg:grid-cols-[1fr,380px] gap-8">
          {/* Left column */}
          <div className="space-y-6">
            {/* Image gallery */}
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="relative">
              <div className="aspect-[16/10] rounded-xl overflow-hidden glass">
                <img
                  src={vehicle.images[selectedImg]}
                  alt={title}
                  className="w-full h-full object-cover"
                />
              </div>
              {vehicle.images.length > 1 && (
                <>
                  <button
                    onClick={() => setSelectedImg(i => (i - 1 + vehicle.images.length) % vehicle.images.length)}
                    className="absolute left-3 top-1/2 -translate-y-1/2 w-10 h-10 glass rounded-full flex items-center justify-center text-foreground"
                  >
                    <ChevronLeft className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => setSelectedImg(i => (i + 1) % vehicle.images.length)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 w-10 h-10 glass rounded-full flex items-center justify-center text-foreground"
                  >
                    <ChevronRight className="w-5 h-5" />
                  </button>
                </>
              )}
              <div className="flex gap-2 mt-3">
                {vehicle.images.map((img, i) => (
                  <button
                    key={i}
                    onClick={() => setSelectedImg(i)}
                    className={`w-20 h-14 rounded-lg overflow-hidden border-2 transition-colors ${
                      i === selectedImg ? "border-primary" : "border-transparent opacity-60 hover:opacity-100"
                    }`}
                  >
                    <img src={img} alt="" className="w-full h-full object-cover" />
                  </button>
                ))}
              </div>
            </motion.div>

            {/* Specs grid */}
            <div className="glass rounded-xl p-6">
              <h3 className="font-semibold mb-4">Technical Specifications</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {specs.map(s => (
                  <div key={s.label} className="space-y-1">
                    <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
                      <s.icon className="w-3.5 h-3.5" />
                      {s.label}
                    </div>
                    <p className="font-medium text-sm">{s.value}</p>
                  </div>
                ))}
              </div>

              <div className="mt-4 pt-4 border-t border-border/30 grid grid-cols-2 gap-4">
                <div>
                  <span className="text-xs text-muted-foreground">City MPG</span>
                  <p className="font-medium text-sm">{vehicle.mpg_city} {vehicle.fuel_type === "Electric" ? "MPGe" : "MPG"}</p>
                </div>
                <div>
                  <span className="text-xs text-muted-foreground">Highway MPG</span>
                  <p className="font-medium text-sm">{vehicle.mpg_highway} {vehicle.fuel_type === "Electric" ? "MPGe" : "MPG"}</p>
                </div>
              </div>
            </div>

            {/* Description */}
            <div className="glass rounded-xl p-6">
              <h3 className="font-semibold mb-2">Description</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{vehicle.description}</p>
              <p className="text-xs text-muted-foreground mt-4">VIN: {vehicle.vin}</p>
            </div>
          </div>

          {/* Right column */}
          <div className="space-y-4">
            <div className="glass rounded-xl p-6 space-y-4 sticky top-24">
              {vehicle.is_anomaly && (
                <div className={`flex items-start gap-2 p-3 rounded-lg ${
                  vehicle.anomaly_severity === "high"
                    ? "bg-destructive/10 border border-destructive/20"
                    : "bg-amber-500/10 border border-amber-500/20"
                }`}>
                  {vehicle.anomaly_severity === "high"
                    ? <ShieldAlert className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
                    : <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                  }
                  <div>
                    <p className="text-sm font-medium text-foreground">
                      {vehicle.anomaly_severity === "high" ? "High Risk Listing" : "Price Anomaly Detected"}
                    </p>
                    <p className="text-xs text-muted-foreground mt-0.5">
                      {vehicle.anomaly_severity === "high"
                        ? "This listing's price is significantly below market value. Proceed with caution."
                        : "The price seems unusual for this vehicle's specs. Verify before purchasing."}
                    </p>
                  </div>
                </div>
              )}

              <div>
                <h2 className="text-xl font-bold">{title}</h2>
                <p className="text-sm text-muted-foreground flex items-center gap-1 mt-1">
                  <MapPin className="w-3.5 h-3.5" /> {vehicle.location}
                </p>
              </div>

              <div className="text-3xl font-extrabold text-gradient">
                ${vehicle.price.toLocaleString()}
              </div>

              <div className="text-xs text-muted-foreground space-y-1">
                <p>Listed by: {vehicle.seller}</p>
                <p>Listed: {new Date(vehicle.listed_date).toLocaleDateString()}</p>
              </div>

              <Button className="w-full" size="lg" onClick={() => setNegoOpen(true)}>
                <MessageSquare className="w-4 h-4 mr-2" />
                Negotiate with AI
              </Button>

              {/* AI Insights */}
              <div className="glass rounded-xl p-4 space-y-2">
                <div className="flex items-center gap-2 text-sm font-semibold">
                  <Sparkles className="w-4 h-4 text-primary" />
                  AI Insights
                </div>
                <ul className="text-xs text-muted-foreground space-y-1.5">
                  <li>• Market value estimate: ${Math.round(vehicle.price * 1.05).toLocaleString()} – ${Math.round(vehicle.price * 1.15).toLocaleString()}</li>
                  <li>• {vehicle.mileage < 5000 ? "Extremely low mileage — likely near-new condition" : `${vehicle.mileage.toLocaleString()} miles is ${vehicle.mileage < 20000 ? "below" : "around"} average for a ${vehicle.year}`}</li>
                  <li>• {vehicle.fuel_type === "Electric" ? "EV — no gas costs, lower maintenance" : `Estimated ${vehicle.mpg_city}/${vehicle.mpg_highway} MPG`}</li>
                  <li>• Similar vehicles sell within 14 days on average</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <NegotiationPanel
        vehicleId={vehicle.id}
        vehicleTitle={title}
        askingPrice={vehicle.price}
        open={negoOpen}
        onClose={() => setNegoOpen(false)}
      />
    </>
  );
}
