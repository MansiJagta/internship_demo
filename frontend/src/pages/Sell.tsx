import { useState } from "react";
import { motion } from "framer-motion";
import { Upload, ChevronRight, ChevronLeft, Check, Car, DollarSign, FileText, Image } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";

const steps = [
  { label: "Vehicle Info", icon: Car },
  { label: "Photos", icon: Image },
  { label: "Details", icon: FileText },
  { label: "Pricing", icon: DollarSign },
];

export default function Sell() {
  const [step, setStep] = useState(0);
  const [form, setForm] = useState({
    make: "", model: "", year: "", mileage: "", fuel_type: "", transmission: "",
    exterior_color: "", interior_color: "", description: "", price: "", hidden_min_price: "", vin: "", location: "",
  });

  const update = (field: string, value: string) => setForm(prev => ({ ...prev, [field]: value }));

  const handleSubmit = () => {
    toast.success("Listing submitted for review!");
    setStep(0);
    setForm({ make: "", model: "", year: "", mileage: "", fuel_type: "", transmission: "", exterior_color: "", interior_color: "", description: "", price: "", hidden_min_price: "", vin: "", location: "" });
  };

  return (
    <div className="container py-8 max-w-2xl">
      <h1 className="text-2xl font-bold mb-8">List Your Vehicle</h1>

      {/* Stepper */}
      <div className="flex items-center gap-2 mb-8">
        {steps.map((s, i) => {
          const StepIcon = s.icon;
          return (
            <div key={s.label} className="flex items-center gap-2 flex-1">
              <div className={`w-9 h-9 rounded-full flex items-center justify-center text-sm font-medium shrink-0 transition-colors ${
                i < step ? "bg-primary text-primary-foreground" :
                i === step ? "bg-primary/20 text-primary border border-primary/40" :
                "bg-muted text-muted-foreground"
              }`}>
                {i < step ? <Check className="w-4 h-4" /> : <StepIcon className="w-4 h-4" />}
              </div>
              {i < steps.length - 1 && (
                <div className={`flex-1 h-px ${i < step ? "bg-primary" : "bg-border"}`} />
              )}
            </div>
          );
        })}
      </div>

      <motion.div
        key={step}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        className="glass rounded-xl p-6 space-y-4"
      >
        {step === 0 && (
          <>
            <h2 className="font-semibold">Vehicle Information</h2>
            <div className="grid grid-cols-2 gap-4">
              <Input placeholder="Make (e.g. Tesla)" value={form.make} onChange={e => update("make", e.target.value)} />
              <Input placeholder="Model (e.g. Model 3)" value={form.model} onChange={e => update("model", e.target.value)} />
              <Input placeholder="Year" type="number" value={form.year} onChange={e => update("year", e.target.value)} />
              <Input placeholder="Mileage" type="number" value={form.mileage} onChange={e => update("mileage", e.target.value)} />
              <Input placeholder="Fuel Type" value={form.fuel_type} onChange={e => update("fuel_type", e.target.value)} />
              <Input placeholder="Transmission" value={form.transmission} onChange={e => update("transmission", e.target.value)} />
            </div>
          </>
        )}

        {step === 1 && (
          <>
            <h2 className="font-semibold">Photos</h2>
            <div className="grid grid-cols-2 gap-4">
              {Array.from({ length: 4 }).map((_, i) => (
                <div
                  key={i}
                  className="aspect-[4/3] rounded-xl border-2 border-dashed border-border/50 flex flex-col items-center justify-center gap-2 text-muted-foreground hover:border-primary/40 hover:text-primary/60 transition-colors cursor-pointer"
                >
                  <Upload className="w-6 h-6" />
                  <span className="text-xs">Upload Photo {i + 1}</span>
                </div>
              ))}
            </div>
          </>
        )}

        {step === 2 && (
          <>
            <h2 className="font-semibold">Details</h2>
            <div className="grid grid-cols-2 gap-4">
              <Input placeholder="Exterior Color" value={form.exterior_color} onChange={e => update("exterior_color", e.target.value)} />
              <Input placeholder="Interior Color" value={form.interior_color} onChange={e => update("interior_color", e.target.value)} />
              <Input placeholder="VIN" value={form.vin} onChange={e => update("vin", e.target.value)} className="col-span-2" />
              <Input placeholder="Location" value={form.location} onChange={e => update("location", e.target.value)} className="col-span-2" />
            </div>
            <Textarea
              placeholder="Describe your vehicle — condition, features, history..."
              value={form.description}
              onChange={e => update("description", e.target.value)}
              rows={5}
            />
          </>
        )}

        {step === 3 && (
          <>
            <h2 className="font-semibold">Set Your Price</h2>
            <div className="space-y-2">
              <label className="text-sm text-muted-foreground">Asking Price ($)</label>
              <Input
                type="number"
                placeholder="45000"
                value={form.price}
                onChange={e => update("price", e.target.value)}
                className="text-2xl font-bold h-14"
              />
              <label className="text-sm text-muted-foreground mt-3 block">Hidden Minimum Price ($)</label>
              <Input
                type="number"
                placeholder="42000"
                value={form.hidden_min_price}
                onChange={e => update("hidden_min_price", e.target.value)}
              />
              <p className="text-xs text-muted-foreground">
                The hidden minimum is protected and used by the AI negotiator to avoid under-selling.
              </p>
            </div>
          </>
        )}
      </motion.div>

      <div className="flex justify-between mt-6">
        <Button variant="outline" disabled={step === 0} onClick={() => setStep(s => s - 1)}>
          <ChevronLeft className="w-4 h-4 mr-1" /> Back
        </Button>
        {step < steps.length - 1 ? (
          <Button onClick={() => setStep(s => s + 1)}>
            Next <ChevronRight className="w-4 h-4 ml-1" />
          </Button>
        ) : (
          <Button onClick={handleSubmit}>
            <Check className="w-4 h-4 mr-1" /> Submit Listing
          </Button>
        )}
      </div>
    </div>
  );
}
