# from datetime import datetime
# from typing import List, Optional

# from pydantic import BaseModel, Field


# # --- Vehicle Schema ---
# class Vehicle(BaseModel):
#     make: str = Field(..., example="Toyota")
#     model: str = Field(..., example="Camry")
#     year: int = Field(..., gt=1900)
#     price: float = Field(..., gt=0)
#     mileage: int = Field(..., ge=0)
#     description: str
#     image_url: str

#     # AI & Internal Logic (Crucial for the assessment)
#     min_acceptable_price: float  # Not shown to buyers
#     embedding: Optional[List[float]] = None  # For Semantic Search
#     is_suspicious: bool = False  # For Anomaly Detection

#     created_at: datetime = Field(default_factory=datetime.utcnow)


# # --- Negotiation Schema ---
# class Message(BaseModel):
#     role: str  # "user" or "assistant"
#     content: str
#     timestamp: datetime = Field(default_factory=datetime.utcnow)


# class Negotiation(BaseModel):
#     vehicle_id: str
#     buyer_id: str
#     status: str = "active"  # active, accepted, rejected
#     current_offer: float
#     chat_history: List[Message] = []













from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, EmailStr

# --- Vehicle Schema ---
class Vehicle(BaseModel):
    make: str
    model: str
    year: int
    price: float
    mileage: int
    description: str
    image_url: str
    min_acceptable_price: float 
    embedding: Optional[List[float]] = None 
    is_suspicious: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

# --- Auth Schemas ---
UserRole = Literal["buyer", "seller"]

class SignupRequest(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserRole

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: UserRole

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic

# --- Negotiation Schema ---
class Message(BaseModel):
    role: str # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Negotiation(BaseModel):
    vehicle_id: str
    buyer_id: str
    status: str = "active"
    current_offer: float
    chat_history: List[Message] = []