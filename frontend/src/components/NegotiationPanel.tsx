import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Send, Bot, User, MessageSquare } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { submitNegotiation } from "@/lib/api";
import type { ChatMessage } from "@/lib/mockData";
import { toast } from "sonner";

interface Props {
  vehicleId: string;
  vehicleTitle: string;
  askingPrice: number;
  open: boolean;
  onClose: () => void;
}

export default function NegotiationPanel({ vehicleId, vehicleTitle, askingPrice, open, onClose }: Props) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [offerPrice, setOfferPrice] = useState(Math.round(askingPrice * 0.9));
  const [inputMsg, setInputMsg] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, isTyping]);

  const handleSend = async () => {
    const msg = inputMsg.trim() || `I'd like to offer $${offerPrice.toLocaleString()} for this vehicle.`;
    const userMsg: ChatMessage = {
      id: `u-${Date.now()}`, sender: "user", message: msg, timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, userMsg]);
    setInputMsg("");
    setIsTyping(true);

    try {
      const { reply } = await submitNegotiation({
        vehicle_id: vehicleId, message: msg, offer_price: offerPrice,
      });
      setMessages(prev => [...prev, reply]);
      toast.success("Offer Sent Successfully!");
    } catch {
      toast.error("Failed to send offer. Try again.");
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-background/60 backdrop-blur-sm z-40"
            onClick={onClose}
          />
          <motion.div
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ type: "spring", damping: 25, stiffness: 200 }}
            className="fixed right-0 top-0 bottom-0 w-full max-w-md z-50 glass border-l border-border/30 flex flex-col"
          >
            <div className="flex items-center justify-between p-4 border-b border-border/30">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
                  <Bot className="w-4 h-4 text-primary" />
                </div>
                <div>
                  <h3 className="font-semibold text-sm">AI Negotiator</h3>
                  <p className="text-xs text-muted-foreground">Negotiating for {vehicleTitle}</p>
                </div>
              </div>
              <button onClick={onClose} className="p-2 rounded-lg hover:bg-muted/50 text-muted-foreground">
                <X className="w-4 h-4" />
              </button>
            </div>

            <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.length === 0 && (
                <div className="flex flex-col items-center justify-center h-full text-center gap-3 text-muted-foreground">
                  <MessageSquare className="w-10 h-10 text-primary/40" />
                  <p className="text-sm">Set your offer price and send a message to start negotiating.</p>
                </div>
              )}

              {messages.map(msg => (
                <motion.div
                  key={msg.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex gap-2 ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
                >
                  {msg.sender === "ai" && (
                    <div className="w-7 h-7 rounded-full bg-primary/20 flex items-center justify-center shrink-0 mt-1">
                      <Bot className="w-3.5 h-3.5 text-primary" />
                    </div>
                  )}
                  <div className={`max-w-[75%] rounded-2xl px-4 py-2.5 text-sm ${
                    msg.sender === "user"
                      ? "bg-primary text-primary-foreground rounded-br-md"
                      : "bg-muted text-foreground rounded-bl-md"
                  }`}>
                    {msg.message}
                  </div>
                  {msg.sender === "user" && (
                    <div className="w-7 h-7 rounded-full bg-muted flex items-center justify-center shrink-0 mt-1">
                      <User className="w-3.5 h-3.5" />
                    </div>
                  )}
                </motion.div>
              ))}

              {isTyping && (
                <div className="flex gap-2">
                  <div className="w-7 h-7 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
                    <Bot className="w-3.5 h-3.5 text-primary" />
                  </div>
                  <div className="bg-muted rounded-2xl rounded-bl-md px-4 py-3 flex gap-1">
                    <span className="w-2 h-2 rounded-full bg-muted-foreground animate-typing-dot-1" />
                    <span className="w-2 h-2 rounded-full bg-muted-foreground animate-typing-dot-2" />
                    <span className="w-2 h-2 rounded-full bg-muted-foreground animate-typing-dot-3" />
                  </div>
                </div>
              )}
            </div>

            <div className="p-4 border-t border-border/30 space-y-4">
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Your Offer</span>
                  <span className="font-bold text-primary text-lg">${offerPrice.toLocaleString()}</span>
                </div>
                <Slider
                  value={[offerPrice]}
                  onValueChange={([v]) => setOfferPrice(v)}
                  min={Math.round(askingPrice * 0.5)}
                  max={askingPrice}
                  step={500}
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-muted-foreground">
                  <span>${Math.round(askingPrice * 0.5).toLocaleString()}</span>
                  <span>Asking: ${askingPrice.toLocaleString()}</span>
                </div>
              </div>

              <div className="flex gap-2">
                <input
                  value={inputMsg}
                  onChange={e => setInputMsg(e.target.value)}
                  onKeyDown={e => e.key === "Enter" && !e.shiftKey && handleSend()}
                  placeholder="Add a message..."
                  className="flex-1 bg-muted/50 border border-border/30 rounded-lg px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary/50"
                />
                <Button size="icon" onClick={handleSend} disabled={isTyping}>
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
