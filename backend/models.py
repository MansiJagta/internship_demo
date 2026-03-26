from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, EmailStr

# --- Vehicle Schema (matches frontend Vehicle interface) ---
class Vehicle(BaseModel):
    make: str
    model: str
    year: int
    price: float
    mileage: int
    description: str
    # Single image used in cards
    image_url: str
    # Gallery images (list)
    images: List[str] = []
    # Spec fields
    fuel_type: str = "Gasoline"
    transmission: str = "Automatic"
    engine: str = ""
    horsepower: int = 200
    drivetrain: str = "FWD"
    exterior_color: str = ""
    interior_color: str = ""
    mpg_city: int = 20
    mpg_highway: int = 28
    # Location / seller info
    seller: str = "AutoVibe Certified"
    location: str = "United States"
    listed_date: str = ""
    vin: str = ""
    # AI fields
    min_acceptable_price: float
    embedding: Optional[List[float]] = None
    is_suspicious: bool = False
    # Anomaly fields (mapped from is_suspicious for the frontend)
    is_anomaly: bool = False
    anomaly_severity: Optional[str] = None  # "high" | "medium"

    created_at: datetime = Field(default_factory=datetime.utcnow)

# --- Auth Schemas ---
UserRole = Literal["buyer", "seller", "admin"]

class SignupRequest(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: Literal["buyer", "seller"]

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic

# --- Negotiation / Chat ---
class ChatMessage(BaseModel):
    id: str
    sender: str  # "user" | "ai"
    message: str
    timestamp: str

class NegotiationRequest(BaseModel):
    vehicle_id: str
    message: str
    offer_price: float

class NegotiationChatResponse(BaseModel):
    success: bool
    reply: ChatMessage

# --- Offers (buyer's negotiations) ---
class Offer(BaseModel):
    id: str
    vehicle_id: str
    vehicle_title: str
    vehicle_image: str
    offer_price: float
    asking_price: float
    status: str  # pending | accepted | countered | rejected
    counter_price: Optional[float] = None
    created_at: str
    updated_at: str

# --- Seller Listings ---
class SellerListing(BaseModel):
    listing_id: str
    vehicle: str
    ai_chat_count: int
    asking_price: float

class ListingRequest(BaseModel):
    make: str
    model: str
    year: int
    mileage: int
    fuel_type: str = "Gasoline"
    transmission: str = "Automatic"
    exterior_color: str = ""
    interior_color: str = ""
    vin: str = ""
    location: str = ""
    description: str = ""
    price: float
    hidden_min_price: float

# --- Vehicle list / search response ---
class VehicleSearchResponse(BaseModel):
    id: str
    make: str
    model: str
    year: int
    price: float
    mileage: int
    description: str
    image_url: str
    images: List[str] = []
    fuel_type: str = "Gasoline"
    transmission: str = "Automatic"
    engine: str = ""
    horsepower: int = 200
    drivetrain: str = "FWD"
    exterior_color: str = ""
    interior_color: str = ""
    mpg_city: int = 20
    mpg_highway: int = 28
    seller: str = "AutoVibe Certified"
    location: str = ""
    listed_date: str = ""
    vin: str = ""
    is_anomaly: bool = False
    anomaly_severity: Optional[str] = None
    is_suspicious: bool = False