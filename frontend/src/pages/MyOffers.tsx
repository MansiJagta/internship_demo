import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { Clock, CheckCircle2, MessageSquare, XCircle } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import { fetchOffers } from "@/lib/api";
import { Link } from "react-router-dom";

const statusConfig = {
  pending: { label: "Pending", class: "status-pending", icon: Clock },
  accepted: { label: "Accepted", class: "status-accepted", icon: CheckCircle2 },
  countered: { label: "Countered", class: "status-countered", icon: MessageSquare },
  rejected: { label: "Rejected", class: "status-rejected", icon: XCircle },
};

export default function MyOffers() {
  const { data: offers, isLoading } = useQuery({
    queryKey: ["offers"],
    queryFn: fetchOffers,
  });

  return (
    <div className="container py-8 max-w-4xl">
      <h1 className="text-2xl font-bold mb-6">My Offers</h1>

      {isLoading ? (
        <div className="space-y-4">
          {Array.from({ length: 3 }).map((_, i) => (
            <Skeleton key={i} className="h-24 w-full rounded-xl" />
          ))}
        </div>
      ) : offers && offers.length > 0 ? (
        <div className="space-y-4">
          {offers.map((offer, i) => {
            const cfg = statusConfig[offer.status];
            const StatusIcon = cfg.icon;
            return (
              <motion.div
                key={offer.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
              >
                <Link
                  to={`/vehicle/${offer.vehicle_id}`}
                  className="glass rounded-xl p-4 flex items-center gap-4 glass-hover block"
                >
                  <img
                    src={offer.vehicle_image}
                    alt={offer.vehicle_title}
                    className="w-20 h-14 rounded-lg object-cover shrink-0"
                  />
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-sm truncate">{offer.vehicle_title}</h3>
                    <p className="text-xs text-muted-foreground mt-0.5">
                      Your offer: <span className="text-foreground font-medium">${offer.offer_price.toLocaleString()}</span>
                      {" · "}Asking: ${offer.asking_price.toLocaleString()}
                    </p>
                    {offer.counter_price && (
                      <p className="text-xs text-primary mt-0.5">
                        Counter: ${offer.counter_price.toLocaleString()}
                      </p>
                    )}
                  </div>
                  <div className="shrink-0">
                    <span className={cfg.class}>
                      <StatusIcon className="w-3 h-3" />
                      {cfg.label}
                    </span>
                  </div>
                </Link>
              </motion.div>
            );
          })}
        </div>
      ) : (
        <div className="text-center py-20 text-muted-foreground">
          <p>No offers yet. Start browsing vehicles to make your first offer.</p>
          <Link to="/browse" className="text-primary hover:underline mt-2 inline-block">Browse Vehicles</Link>
        </div>
      )}
    </div>
  );
}
