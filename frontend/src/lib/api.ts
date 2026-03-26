import axios from "axios";
import { vehicles, offers, type Vehicle, type Offer, type ChatMessage } from "./mockData";

const api = axios.create({ baseURL: "http://localhost:8000" });

export type UserRole = "buyer" | "seller";

export interface AuthUser {
  id: string;
  name: string;
  email: string;
  role: UserRole;
}

export interface AuthResponse {
  access_token: string;
  token_type: "bearer";
  user: AuthUser;
}

export interface SellerListing {
  listing_id: string;
  vehicle: string;
  ai_chat_count: number;
  asking_price: number;
}

export function setAuthToken(token: string | null) {
  if (token) {
    api.defaults.headers.common.Authorization = `Bearer ${token}`;
    return;
  }
  delete api.defaults.headers.common.Authorization;
}

export async function signup(body: {
  name: string;
  email: string;
  password: string;
  role: UserRole;
}): Promise<AuthResponse> {
  const { data } = await api.post("/auth/signup", body);
  return data;
}

export async function login(body: {
  email: string;
  password: string;
}): Promise<AuthResponse> {
  const { data } = await api.post("/auth/login", body);
  return data;
}

export async function fetchMe(): Promise<AuthUser> {
  const { data } = await api.get("/auth/me");
  return data;
}

// Simulated API calls using mock data (replace with real API when backend is ready)
export async function fetchVehicles(params?: {
  make?: string; model?: string; min_price?: number; max_price?: number;
  min_year?: number; max_year?: number; max_mileage?: number; page?: number;
}): Promise<Vehicle[]> {
  try {
    const { data } = await api.get("/vehicles", { params });
    return data;
  } catch {
    // Fallback to mock data
    let results = [...vehicles];
    if (params?.make) results = results.filter(v => v.make.toLowerCase().includes(params.make!.toLowerCase()));
    if (params?.model) results = results.filter(v => v.model.toLowerCase().includes(params.model!.toLowerCase()));
    if (params?.min_price) results = results.filter(v => v.price >= params.min_price!);
    if (params?.max_price) results = results.filter(v => v.price <= params.max_price!);
    if (params?.min_year) results = results.filter(v => v.year >= params.min_year!);
    if (params?.max_year) results = results.filter(v => v.year <= params.max_year!);
    if (params?.max_mileage) results = results.filter(v => v.mileage <= params.max_mileage!);
    return results;
  }
}

export async function fetchVehicle(id: string): Promise<Vehicle | undefined> {
  try {
    const { data } = await api.get(`/vehicles/${id}`);
    return data;
  } catch {
    return vehicles.find(v => v.id === id);
  }
}

export async function semanticSearch(query: string): Promise<Vehicle[]> {
  try {
    const { data } = await api.post("/search/semantic", null, { params: { query } });
    return data;
  } catch {
    // Simulate semantic search with keyword matching
    await new Promise(r => setTimeout(r, 1500));
    const q = query.toLowerCase();
    return vehicles.filter(v =>
      v.make.toLowerCase().includes(q) || v.model.toLowerCase().includes(q) ||
      v.description.toLowerCase().includes(q) || v.fuel_type.toLowerCase().includes(q) ||
      v.exterior_color.toLowerCase().includes(q)
    );
  }
}

export async function submitNegotiation(body: {
  vehicle_id: string; message: string; offer_price: number;
}): Promise<{ success: boolean; reply: ChatMessage }> {
  try {
    const { data } = await api.post("/negotiate", body);
    return data;
  } catch {
    await new Promise(r => setTimeout(r, 2000));
    const replies = [
      "I appreciate your offer. Let me check with the seller and get back to you shortly.",
      "That's an interesting proposal. The seller is reviewing your offer now.",
      "Thank you for your interest! Based on market analysis, I'd suggest we meet in the middle.",
    ];
    return {
      success: true,
      reply: {
        id: `r-${Date.now()}`,
        sender: "ai",
        message: replies[Math.floor(Math.random() * replies.length)],
        timestamp: new Date().toISOString(),
      },
    };
  }
}

export async function fetchOffers(): Promise<Offer[]> {
  try {
    const { data } = await api.get("/offers");
    return data;
  } catch {
    return offers;
  }
}

export async function fetchMyListings(): Promise<SellerListing[]> {
  try {
    const { data } = await api.get("/seller/listings");
    return data;
  } catch {
    return [
      {
        listing_id: "listing-fallback-1",
        vehicle: "2021 BMW X5",
        ai_chat_count: 3,
        asking_price: 48900,
      },
    ];
  }
}

export interface CreateListingPayload {
  make: string;
  model: string;
  year: number;
  mileage: number;
  fuel_type: string;
  transmission: string;
  exterior_color: string;
  interior_color: string;
  vin: string;
  location: string;
  description: string;
  price: number;
  hidden_min_price: number;
}

export async function createListing(body: CreateListingPayload): Promise<{ listing_id: string; message: string }> {
  const { data } = await api.post("/seller/listings", body);
  return data;
}
