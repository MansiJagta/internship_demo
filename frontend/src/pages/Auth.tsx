import { FormEvent, useMemo, useState } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Car, CircleUserRound, Store } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/hooks/useAuth";
import type { UserRole } from "@/lib/api";
import { toast } from "sonner";

type AuthMode = "login" | "signup";

export default function Auth() {
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated, user, loginUser, signupUser } = useAuth();

  const [mode, setMode] = useState<AuthMode>("login");
  const [role, setRole] = useState<UserRole>("buyer");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const redirectTo = useMemo(() => {
    const from = (location.state as { from?: string } | null)?.from;
    if (from) return from;
    if (user?.role === "seller") return "/my-listings";
    return "/my-offers";
  }, [location.state, user?.role]);

  if (isAuthenticated) {
    return <Navigate to={redirectTo} replace />;
  }

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitting(true);

    try {
      if (mode === "signup") {
        await signupUser({ name, email, password, role });
        toast.success("Account created successfully");
      } else {
        await loginUser({ email, password });
        toast.success("Welcome back");
      }

      navigate(redirectTo, { replace: true });
    } catch {
      toast.error("Authentication failed. Please check your credentials.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="container py-10 md:py-16">
      <div className="mx-auto max-w-5xl grid md:grid-cols-2 gap-8 items-stretch">
        <motion.section
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass rounded-2xl p-8 relative overflow-hidden"
        >
          <div className="absolute -top-12 -right-12 w-48 h-48 rounded-full bg-primary/20 blur-3xl" />
          <h1 className="text-3xl font-bold leading-tight">Choose your lane</h1>
          <p className="text-muted-foreground mt-3">
            Buyers find the best deal through AI negotiation. Sellers list inventory and let the AI handle first-round haggling.
          </p>

          <div className="mt-8 space-y-4">
            <div className="rounded-xl border border-border/50 bg-card/50 p-4 flex gap-3">
              <CircleUserRound className="w-5 h-5 text-primary shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold">Buyer (Standard User)</p>
                <p className="text-sm text-muted-foreground">Browse listings, use semantic search, and track active negotiations in My Offers.</p>
              </div>
            </div>
            <div className="rounded-xl border border-border/50 bg-card/50 p-4 flex gap-3">
              <Store className="w-5 h-5 text-primary shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold">Seller (Individual/Dealer)</p>
                <p className="text-sm text-muted-foreground">Upload inventory, define hidden minimum price, and monitor engagement in My Listings.</p>
              </div>
            </div>
          </div>
        </motion.section>

        <motion.section
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass rounded-2xl p-8"
        >
          <div className="flex items-center gap-2 text-lg font-bold mb-6">
            <Car className="w-5 h-5 text-primary" />
            AutoVibe Account
          </div>

          <div className="inline-flex rounded-lg bg-muted p-1 mb-6">
            <button
              onClick={() => setMode("login")}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                mode === "login" ? "bg-background text-foreground" : "text-muted-foreground"
              }`}
            >
              Login
            </button>
            <button
              onClick={() => setMode("signup")}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                mode === "signup" ? "bg-background text-foreground" : "text-muted-foreground"
              }`}
            >
              Sign Up
            </button>
          </div>

          <form className="space-y-4" onSubmit={submit}>
            {mode === "signup" && (
              <Input
                placeholder="Full name"
                value={name}
                onChange={e => setName(e.target.value)}
                required
              />
            )}
            <Input
              type="email"
              placeholder="Email address"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
            />
            <Input
              type="password"
              placeholder="Password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              minLength={6}
              required
            />

            {mode === "signup" && (
              <div>
                <p className="text-sm text-muted-foreground mb-2">I am signing up as:</p>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    type="button"
                    onClick={() => setRole("buyer")}
                    className={`rounded-lg border p-3 text-left transition-colors ${
                      role === "buyer"
                        ? "border-primary bg-primary/10"
                        : "border-border/50 hover:border-border"
                    }`}
                  >
                    <p className="font-medium">Buyer</p>
                    <p className="text-xs text-muted-foreground">Negotiates and tracks offers</p>
                  </button>
                  <button
                    type="button"
                    onClick={() => setRole("seller")}
                    className={`rounded-lg border p-3 text-left transition-colors ${
                      role === "seller"
                        ? "border-primary bg-primary/10"
                        : "border-border/50 hover:border-border"
                    }`}
                  >
                    <p className="font-medium">Seller</p>
                    <p className="text-xs text-muted-foreground">Lists cars and tracks AI chats</p>
                  </button>
                </div>
              </div>
            )}

            <Button className="w-full" type="submit" disabled={submitting}>
              {submitting ? "Please wait..." : mode === "signup" ? "Create account" : "Login"}
            </Button>
          </form>
        </motion.section>
      </div>
    </div>
  );
}
