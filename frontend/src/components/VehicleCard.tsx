import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { MapPin, Gauge, Fuel, AlertTriangle, ShieldAlert } from "lucide-react";
import type { Vehicle } from "@/lib/mockData";

export default function VehicleCard({ vehicle, index = 0 }: { vehicle: Vehicle; index?: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.05 }}
    >
      <Link
        to={`/vehicle/${vehicle.id}`}
        className="group block glass rounded-xl overflow-hidden glass-hover"
      >
        <div className="relative aspect-[16/10] overflow-hidden">
          <img
            src={vehicle.image}
            alt={`${vehicle.year} ${vehicle.make} ${vehicle.model}`}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
            loading="lazy"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-background/80 via-transparent to-transparent" />

          {vehicle.is_anomaly && (
            <div className="absolute top-3 right-3">
              <span className={vehicle.anomaly_severity === "high" ? "badge-anomaly-high" : "badge-anomaly-medium"}>
                {vehicle.anomaly_severity === "high" ? (
                  <ShieldAlert className="w-3 h-3" />
                ) : (
                  <AlertTriangle className="w-3 h-3" />
                )}
                Suspicious
              </span>
            </div>
          )}

          <div className="absolute bottom-3 left-3">
            <span className="text-2xl font-bold text-foreground">
              ${vehicle.price.toLocaleString()}
            </span>
          </div>
        </div>

        <div className="p-4 space-y-3">
          <div>
            <h3 className="font-semibold text-foreground group-hover:text-primary transition-colors">
              {vehicle.year} {vehicle.make} {vehicle.model}
            </h3>
            <p className="text-sm text-muted-foreground flex items-center gap-1 mt-1">
              <MapPin className="w-3 h-3" />
              {vehicle.location}
            </p>
          </div>

          <div className="flex items-center gap-4 text-xs text-muted-foreground">
            <span className="flex items-center gap-1">
              <Gauge className="w-3.5 h-3.5" />
              {vehicle.mileage.toLocaleString()} mi
            </span>
            <span className="flex items-center gap-1">
              <Fuel className="w-3.5 h-3.5" />
              {vehicle.fuel_type}
            </span>
            <span>{vehicle.transmission}</span>
          </div>
        </div>
      </Link>
    </motion.div>
  );
}
