import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { MessageCircleMore, DollarSign, CarFront } from "lucide-react";
import { fetchMyListings } from "@/lib/api";
import { Skeleton } from "@/components/ui/skeleton";

export default function MyListings() {
  const { data: listings, isLoading } = useQuery({
    queryKey: ["my-listings"],
    queryFn: fetchMyListings,
  });

  return (
    <div className="container py-8 max-w-4xl">
      <h1 className="text-2xl font-bold mb-6">My Listings</h1>

      {isLoading ? (
        <div className="space-y-4">
          {Array.from({ length: 3 }).map((_, idx) => (
            <Skeleton key={idx} className="h-28 rounded-xl" />
          ))}
        </div>
      ) : listings && listings.length > 0 ? (
        <div className="space-y-4">
          {listings.map((listing, index) => (
            <motion.div
              key={listing.listing_id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className="glass rounded-xl p-5"
            >
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="font-semibold text-lg">{listing.vehicle}</p>
                  <p className="text-sm text-muted-foreground mt-1">Listing ID: {listing.listing_id}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-muted-foreground">Asking Price</p>
                  <p className="font-semibold text-xl">${listing.asking_price.toLocaleString()}</p>
                </div>
              </div>

              <div className="mt-4 grid sm:grid-cols-3 gap-3">
                <div className="rounded-lg bg-muted/40 p-3 flex items-center gap-2">
                  <CarFront className="w-4 h-4 text-primary" />
                  <span className="text-sm">Active listing</span>
                </div>
                <div className="rounded-lg bg-muted/40 p-3 flex items-center gap-2">
                  <MessageCircleMore className="w-4 h-4 text-primary" />
                  <span className="text-sm">{listing.ai_chat_count} AI chats</span>
                </div>
                <div className="rounded-lg bg-muted/40 p-3 flex items-center gap-2">
                  <DollarSign className="w-4 h-4 text-primary" />
                  <span className="text-sm">Negotiator active</span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      ) : (
        <div className="text-center py-16 text-muted-foreground">
          No listings yet. Add your first vehicle from the Sell page.
        </div>
      )}
    </div>
  );
}
