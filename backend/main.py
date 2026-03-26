# # from datetime import datetime, timedelta, timezone
# # from typing import Any, Literal
# # import os

# # import jwt
# # from fastapi import Depends, FastAPI, HTTPException, status
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
# # from passlib.context import CryptContext
# # from pydantic import BaseModel, EmailStr, Field
# # from database import lifespan

# # app = FastAPI(title="AutoVibe API", version="0.1.0", lifespan=lifespan)

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# # security = HTTPBearer()

# # JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-production")
# # JWT_ALGORITHM = "HS256"
# # JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

# # UserRole = Literal["buyer", "seller"]


# # class SignupRequest(BaseModel):
# #     name: str = Field(min_length=2, max_length=100)
# #     email: EmailStr
# #     password: str = Field(min_length=6, max_length=128)
# #     role: UserRole


# # class LoginRequest(BaseModel):
# #     email: EmailStr
# #     password: str = Field(min_length=6, max_length=128)


# # class UserPublic(BaseModel):
# #     id: str
# #     name: str
# #     email: EmailStr
# #     role: UserRole


# # class AuthResponse(BaseModel):
# #     access_token: str
# #     token_type: str = "bearer"
# #     user: UserPublic


# # # In-memory data store for demo purposes.
# # USERS: dict[str, dict[str, Any]] = {}
# # OFFERS_BY_BUYER: dict[str, list[dict[str, Any]]] = {}
# # LISTINGS_BY_SELLER: dict[str, list[dict[str, Any]]] = {}


# # def hash_password(password: str) -> str:
# #     return pwd_context.hash(password)


# # def verify_password(plain_password: str, hashed_password: str) -> bool:
# #     return pwd_context.verify(plain_password, hashed_password)


# # def create_access_token(user_id: str, role: UserRole, email: str) -> str:
# #     now = datetime.now(timezone.utc)
# #     payload = {
# #         "sub": user_id,
# #         "role": role,
# #         "email": email,
# #         "iat": int(now.timestamp()),
# #         "exp": int((now + timedelta(minutes=JWT_EXPIRE_MINUTES)).timestamp()),
# #     }
# #     return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


# # def get_current_user(
# #     credentials: HTTPAuthorizationCredentials = Depends(security),
# # ) -> dict[str, Any]:
# #     token = credentials.credentials
# #     try:
# #         payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
# #     except jwt.InvalidTokenError as exc:
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="Invalid or expired token",
# #         ) from exc

# #     user_id = payload.get("sub")
# #     if not user_id or user_id not in USERS:
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="User not found",
# #         )
# #     return USERS[user_id]


# # def require_role(expected_role: UserRole):
# #     def _guard(user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
# #         if user["role"] != expected_role:
# #             raise HTTPException(
# #                 status_code=status.HTTP_403_FORBIDDEN,
# #                 detail=f"Only {expected_role}s can access this endpoint",
# #             )
# #         return user

# #     return _guard


# # @app.get("/")
# # async def root() -> dict[str, str]:
# #     return {"message": "AutoVibe API is live!"}


# # @app.get("/health")
# # def health() -> dict[str, str]:
# #     return {"status": "ok"}


# # @app.post("/auth/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
# # def signup(payload: SignupRequest) -> AuthResponse:
# #     normalized_email = payload.email.lower()
# #     if any(user["email"] == normalized_email for user in USERS.values()):
# #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

# #     user_id = f"u-{len(USERS) + 1}"
# #     user = {
# #         "id": user_id,
# #         "name": payload.name.strip(),
# #         "email": normalized_email,
# #         "password_hash": hash_password(payload.password),
# #         "role": payload.role,
# #     }
# #     USERS[user_id] = user

# #     # Seed demo role-specific data so dashboards are not empty.
# #     if payload.role == "buyer":
# #         OFFERS_BY_BUYER[user_id] = [
# #             {
# #                 "id": f"o-{user_id}-1",
# #                 "vehicle_id": "1",
# #                 "vehicle_title": "2022 Tesla Model 3",
# #                 "vehicle_image": "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&q=80",
# #                 "offer_price": 35500,
# #                 "asking_price": 37900,
# #                 "status": "countered",
# #                 "counter_price": 36700,
# #                 "created_at": datetime.now(timezone.utc).isoformat(),
# #                 "updated_at": datetime.now(timezone.utc).isoformat(),
# #                 "messages": [
# #                     {
# #                         "id": f"m-{user_id}-1",
# #                         "sender": "user",
# #                         "message": "Would you accept $35,500?",
# #                         "timestamp": datetime.now(timezone.utc).isoformat(),
# #                     },
# #                     {
# #                         "id": f"m-{user_id}-2",
# #                         "sender": "ai",
# #                         "message": "Seller has countered at $36,700.",
# #                         "timestamp": datetime.now(timezone.utc).isoformat(),
# #                     },
# #                 ],
# #             }
# #         ]
# #     else:
# #         LISTINGS_BY_SELLER[user_id] = [
# #             {
# #                 "listing_id": f"l-{user_id}-1",
# #                 "vehicle": "2021 BMW X5",
# #                 "ai_chat_count": 4,
# #                 "asking_price": 48900,
# #             }
# #         ]

# #     token = create_access_token(user_id=user_id, role=payload.role, email=normalized_email)
# #     return AuthResponse(
# #         access_token=token,
# #         user=UserPublic(id=user_id, name=user["name"], email=normalized_email, role=payload.role),
# #     )


# # @app.post("/auth/login", response_model=AuthResponse)
# # def login(payload: LoginRequest) -> AuthResponse:
# #     normalized_email = payload.email.lower()
# #     user = next((entry for entry in USERS.values() if entry["email"] == normalized_email), None)
# #     if user is None or not verify_password(payload.password, user["password_hash"]):
# #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

# #     token = create_access_token(user_id=user["id"], role=user["role"], email=normalized_email)
# #     return AuthResponse(
# #         access_token=token,
# #         user=UserPublic(id=user["id"], name=user["name"], email=user["email"], role=user["role"]),
# #     )


# # @app.get("/auth/me", response_model=UserPublic)
# # def me(user: dict[str, Any] = Depends(get_current_user)) -> UserPublic:
# #     return UserPublic(id=user["id"], name=user["name"], email=user["email"], role=user["role"])


# # @app.get("/offers")
# # def get_my_offers(user: dict[str, Any] = Depends(require_role("buyer"))) -> list[dict[str, Any]]:
# #     return OFFERS_BY_BUYER.get(user["id"], [])


# # @app.get("/seller/listings")
# # def get_my_listings(user: dict[str, Any] = Depends(require_role("seller"))) -> list[dict[str, Any]]:
# #     return LISTINGS_BY_SELLER.get(user["id"], [])









# import os
# import jwt
# from datetime import datetime, timedelta, timezone
# from typing import Any, Optional
# from fastapi import Depends, FastAPI, HTTPException, status, Query
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
# from passlib.context import CryptContext
# from sentence_transformers import SentenceTransformer

# from database import lifespan, get_vehicle_collection
# from models import SignupRequest, LoginRequest, AuthResponse, UserPublic, UserRole

# app = FastAPI(title="AutoVibe API", lifespan=lifespan)
# model = SentenceTransformer('all-MiniLM-L6-v2')
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# security = HTTPBearer()

# # Auth Settings
# JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-here")
# JWT_ALGORITHM = "HS256"
# JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Mock DB for Auth (for demo purposes)
# USERS: dict[str, dict[str, Any]] = {}

# # --- Auth Helpers ---
# def create_access_token(user_id: str, role: str, email: str) -> str:
#     payload = {
#         "sub": user_id, "role": role, "email": email,
#         "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
#     }
#     return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

# # --- ROUTES ---

# @app.get("/")
# async def root():
#     return {"message": "AutoVibe API is live!"}

# @app.post("/auth/signup", response_model=AuthResponse)
# def signup(payload: SignupRequest):
#     user_id = f"u-{len(USERS) + 1}"
#     user = {
#         "id": user_id, "name": payload.name, "email": payload.email.lower(),
#         "password_hash": pwd_context.hash(payload.password), "role": payload.role
#     }
#     USERS[user_id] = user
#     token = create_access_token(user_id, payload.role, payload.email)
#     return AuthResponse(access_token=token, user=UserPublic(**user))

# @app.get("/vehicles")
# async def list_vehicles(make: Optional[str] = None, page: int = 1):
#     col = get_vehicle_collection()
#     query = {"make": {"$regex": make, "$options": "i"}} if make else {}
#     cursor = col.find(query, {"min_acceptable_price": 0, "embedding": 0}).skip((page-1)*12).limit(12)
#     return await cursor.to_list(length=12)

# @app.post("/search/semantic")
# async def semantic_search(query: str):
#     col = get_vehicle_collection()
#     vector = model.encode(query).tolist()
#     pipeline = [
#         {"$vectorSearch": {
#             "index": "vector_index", # Ensure this name matches Atlas
#             "path": "embedding",
#             "queryVector": vector,
#             "numCandidates": 50,
#             "limit": 6
#         }},
#         {"$project": {"embedding": 0, "min_acceptable_price": 0}}
#     ]
#     return await col.aggregate(pipeline).to_list(length=6)

# @app.post("/negotiate")
# async def negotiate(vehicle_id: str, offer: float):
#     # This is the placeholder for your LangGraph logic
#     if offer < 5000:
#         return {"message": "The seller rejected your offer. It's too low."}
#     return {"message": "The seller is considering your offer. We will get back to you!"}













import os
import bcrypt
import jwt
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, List
from fastapi import Depends, FastAPI, HTTPException, status, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sentence_transformers import SentenceTransformer
from bson import ObjectId
from passlib.context import CryptContext

# --- Python 3.13 bcrypt monkey patch for passlib ---
if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = type("about", (), {"__version__": bcrypt.__version__})

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

from database import lifespan, get_vehicle_collection, get_user_collection, get_negotiations_collection
from models import (
    SignupRequest, LoginRequest, AuthResponse, UserPublic,
    VehicleSearchResponse, NegotiationRequest, NegotiationChatResponse,
    ChatMessage, Offer, SellerListing, ListingRequest
)
from negotiator import negotiator_app
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI(title="AutoVibe API", lifespan=lifespan)
model = SentenceTransformer('all-MiniLM-L6-v2')
security = HTTPBearer()

# --- Password Helpers using passlib PBKDF2 ---
def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# Auth Settings
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-here")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Auth Helpers ---
def create_access_token(user_id: str, role: str, email: str) -> str:
    payload = {
        "sub": user_id, "role": role, "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_col = get_user_collection()
        user = await user_col.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        user["id"] = str(user["_id"])
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# ─────────────────────────────────────────────
# Helper: serialize a vehicle doc from MongoDB
# ─────────────────────────────────────────────
def _serialize_vehicle(v: dict) -> dict:
    v["id"] = str(v.pop("_id"))
    # Ensure images list is populated
    if not v.get("images"):
        v["images"] = [v.get("image_url", "")]
    # Map is_suspicious → is_anomaly for the frontend
    if "is_anomaly" not in v:
        is_sus = v.get("is_suspicious", False)
        v["is_anomaly"] = is_sus
        if is_sus and "anomaly_severity" not in v:
            v["anomaly_severity"] = "medium"
    # Defaults for optional fields
    for field, default in [
        ("fuel_type", "Gasoline"), ("transmission", "Automatic"),
        ("engine", ""), ("horsepower", 200), ("drivetrain", "FWD"),
        ("exterior_color", ""), ("interior_color", ""),
        ("mpg_city", 20), ("mpg_highway", 28),
        ("seller", "AutoVibe Certified"), ("location", "United States"),
        ("listed_date", ""), ("vin", ""),
    ]:
        if field not in v:
            v[field] = default
    return v

# --- ROUTES ---

@app.get("/")
async def root():
    return {"message": "AutoVibe API is live!"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# ── Auth ──────────────────────────────────────

@app.post("/auth/signup", response_model=AuthResponse)
async def signup(payload: SignupRequest):
    user_col = get_user_collection()
    existing_user = await user_col.find_one({"email": payload.email.lower()})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_doc = {
        "name": payload.name,
        "email": payload.email.lower(),
        "password_hash": hash_password(payload.password),
        "role": payload.role,
        "created_at": datetime.utcnow()
    }
    result = await user_col.insert_one(user_doc)
    user_id = str(result.inserted_id)

    token = create_access_token(user_id, payload.role, payload.email)
    return AuthResponse(
        access_token=token,
        user=UserPublic(id=user_id, name=payload.name, email=payload.email, role=payload.role)
    )

@app.post("/auth/login", response_model=AuthResponse)
async def login(payload: LoginRequest):
    user_col = get_user_collection()
    user = await user_col.find_one({"email": payload.email.lower()})

    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user_id = str(user["_id"])
    token = create_access_token(user_id, user["role"], user["email"])
    return AuthResponse(
        access_token=token,
        user=UserPublic(id=user_id, name=user["name"], email=user["email"], role=user["role"])
    )

@app.get("/auth/me", response_model=UserPublic)
async def me(user: dict = Depends(get_current_user)):
    return UserPublic(id=user["id"], name=user["name"], email=user["email"], role=user["role"])

# ── Vehicles ──────────────────────────────────

@app.get("/vehicles")
async def list_vehicles(
    make: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    max_mileage: Optional[int] = None,
    page: int = 1,
    limit: int = 12,
):
    col = get_vehicle_collection()
    query: dict = {}
    if make:
        query["make"] = {"$regex": make, "$options": "i"}
    if min_price is not None or max_price is not None:
        query["price"] = {}
        if min_price is not None:
            query["price"]["$gte"] = min_price
        if max_price is not None:
            query["price"]["$lte"] = max_price
    if min_year is not None or max_year is not None:
        query["year"] = {}
        if min_year is not None:
            query["year"]["$gte"] = min_year
        if max_year is not None:
            query["year"]["$lte"] = max_year
    if max_mileage is not None:
        query["mileage"] = {"$lte": max_mileage}

    cursor = (
        col.find(query, {"min_acceptable_price": 0, "embedding": 0})
        .sort("year", -1)
        .skip((page - 1) * limit)
        .limit(limit)
    )
    vehicles = await cursor.to_list(length=limit)
    return [_serialize_vehicle(v) for v in vehicles]

@app.get("/vehicles/{vehicle_id}")
async def get_vehicle(vehicle_id: str):
    col = get_vehicle_collection()
    try:
        obj_id = ObjectId(vehicle_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid vehicle ID")

    v = await col.find_one({"_id": obj_id}, {"min_acceptable_price": 0, "embedding": 0})
    if not v:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return _serialize_vehicle(v)

# ── Semantic Search ────────────────────────────

@app.post("/search/semantic")
async def semantic_search(query: str):
    col = get_vehicle_collection()
    vector = model.encode(query, normalize_embeddings=True).tolist()
    pipeline = [
        {"$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": vector,
            "numCandidates": 50,
            "limit": 6
        }},
        {"$project": {"embedding": 0, "min_acceptable_price": 0}}
    ]
    try:
        results = await col.aggregate(pipeline).to_list(length=6)
        return [_serialize_vehicle(r) for r in results]
    except Exception:
        # Fallback: keyword search if Atlas vector index not set up
        regex = {"$regex": query, "$options": "i"}
        cursor = col.find(
            {"$or": [{"make": regex}, {"model": regex}, {"description": regex}]},
            {"embedding": 0, "min_acceptable_price": 0}
        ).limit(6)
        results = await cursor.to_list(length=6)
        return [_serialize_vehicle(r) for r in results]

# ── Negotiate ──────────────────────────────────

@app.post("/negotiate", response_model=NegotiationChatResponse)
async def negotiate(
    payload: NegotiationRequest,
    user: dict = Depends(get_current_user)
):
    # Load previous history from DB
    neg_col = get_negotiations_collection()
    existing_neg = await neg_col.find_one({
        "vehicle_id": payload.vehicle_id,
        "buyer_id": ObjectId(user["id"])
    })
    
    history = []
    if existing_neg and "messages" in existing_neg:
        for m in existing_neg["messages"]:
            if m["sender"] == "human":
                history.append(HumanMessage(content=m["message"]))
            else:
                history.append(AIMessage(content=m["message"]))
    
    # Initialize state for LangGraph
    # We append the NEW message to the history
    initial_state = {
        "messages": history + [HumanMessage(content=payload.message)],
        "vehicle_id": payload.vehicle_id,
        "buyer_id": user["id"],
        "offer_amount": payload.offer_price,
        "decision": "PENDING"
    }
    
    # Run the graph
    try:
        final_state = await negotiator_app.ainvoke(initial_state)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Negotiation engine error: {str(e)}")
    
    last_message = final_state["messages"][-1]
    reply_text = last_message.content

    reply = ChatMessage(
        id=f"ai-{uuid.uuid4().hex[:8]}",
        sender="ai",
        message=reply_text,
        timestamp=datetime.utcnow().isoformat(),
    )
    return NegotiationChatResponse(success=True, reply=reply)

# ── Offers (buyer) ────────────────────────────

@app.get("/offers")
async def get_my_offers(user: dict = Depends(get_current_user)):
    neg_col = get_negotiations_collection()
    cursor = neg_col.find(
        {"buyer_id": ObjectId(user["id"])},
    ).sort("timestamp", -1).limit(20)
    docs = await cursor.to_list(length=20)

    offers = []
    for doc in docs:
        offers.append({
            "id": str(doc["_id"]),
            "vehicle_id": doc.get("vehicle_id", ""),
            "vehicle_title": doc.get("vehicle_title", "Unknown Vehicle"),
            "vehicle_image": doc.get("vehicle_image", ""),
            "offer_price": doc.get("offer_price", 0),
            "asking_price": doc.get("asking_price", 0),
            "status": doc.get("status", "pending"),
            "counter_price": doc.get("counter_price"),
            "created_at": doc.get("timestamp", datetime.utcnow()).isoformat() if hasattr(doc.get("timestamp"), "isoformat") else str(doc.get("timestamp", "")),
            "updated_at": doc.get("updated_at", datetime.utcnow()).isoformat() if hasattr(doc.get("updated_at"), "isoformat") else str(doc.get("updated_at", "")),
        })
    return offers

# ── Seller Listings ───────────────────────────

@app.get("/seller/listings")
async def get_my_listings(user: dict = Depends(get_current_user)):
    if user.get("role") not in ("seller", "admin"):
        raise HTTPException(status_code=403, detail="Only sellers can access listings")

    col = get_vehicle_collection()
    cursor = col.find(
        {"seller_id": user["id"]},
        {"embedding": 0}
    ).sort("created_at", -1).limit(50)
    docs = await cursor.to_list(length=50)

    # Count negotiations per vehicle
    neg_col = get_negotiations_collection()
    listings = []
    for doc in docs:
        vid = str(doc["_id"])
        chat_count = await neg_col.count_documents({"vehicle_id": vid})
        listings.append({
            "listing_id": vid,
            "vehicle": f"{doc['year']} {doc['make']} {doc['model']}",
            "ai_chat_count": chat_count,
            "asking_price": doc["price"],
        })
    return listings

@app.post("/seller/listings")
async def create_listing(
    payload: ListingRequest,
    user: dict = Depends(get_current_user)
):
    if user.get("role") not in ("seller", "admin"):
        raise HTTPException(status_code=403, detail="Only sellers can create listings")

    col = get_vehicle_collection()
    now = datetime.utcnow()
    doc = {
        "make": payload.make,
        "model": payload.model,
        "year": payload.year,
        "price": payload.price,
        "mileage": payload.mileage,
        "description": payload.description,
        "fuel_type": payload.fuel_type,
        "transmission": payload.transmission,
        "exterior_color": payload.exterior_color,
        "interior_color": payload.interior_color,
        "vin": payload.vin,
        "location": payload.location,
        "min_acceptable_price": payload.hidden_min_price,
        "image_url": f"https://picsum.photos/seed/{payload.make.lower()}-{payload.year}/900/600",
        "images": [f"https://picsum.photos/seed/{payload.make.lower()}-{payload.year}/900/600"],
        "seller": user["name"],
        "seller_id": user["id"],
        "listed_date": now.strftime("%Y-%m-%d"),
        "is_suspicious": False,
        "is_anomaly": False,
        "embedding": None,
        "created_at": now,
    }
    result = await col.insert_one(doc)
    return {"listing_id": str(result.inserted_id), "message": "Listing created successfully"}
