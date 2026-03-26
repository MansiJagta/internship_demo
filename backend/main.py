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
import jwt
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, List
from fastapi import Depends, FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sentence_transformers import SentenceTransformer
from bson import ObjectId

from database import lifespan, get_vehicle_collection, get_user_collection, get_negotiations_collection
from models import SignupRequest, LoginRequest, AuthResponse, UserPublic, UserRole, VehicleSearchResponse

app = FastAPI(title="AutoVibe API", lifespan=lifespan)
model = SentenceTransformer('all-MiniLM-L6-v2')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

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
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# --- ROUTES ---

@app.get("/")
async def root():
    return {"message": "AutoVibe API is live!"}

@app.post("/auth/signup", response_model=AuthResponse)
async def signup(payload: SignupRequest):
    user_col = get_user_collection()
    existing_user = await user_col.find_one({"email": payload.email.lower()})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_doc = {
        "name": payload.name,
        "email": payload.email.lower(),
        "password_hash": pwd_context.hash(payload.password),
        "role": payload.role,
        "created_at": datetime.utcnow()
    }
    result = await user_col.insert_one(user_doc)
    user_id = str(result.inserted_id)
    
    token = create_access_token(user_id, payload.role, payload.email)
    return AuthResponse(access_token=token, user=UserPublic(id=user_id, **user_doc))

@app.post("/auth/login", response_model=AuthResponse)
async def login(payload: LoginRequest):
    user_col = get_user_collection()
    user = await user_col.find_one({"email": payload.email.lower()})
    
    if not user or not pwd_context.verify(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    user_id = str(user["_id"])
    token = create_access_token(user_id, user["role"], user["email"])
    return AuthResponse(access_token=token, user=UserPublic(id=user_id, **user))

@app.get("/vehicles")
async def list_vehicles(make: Optional[str] = None, page: int = 1):
    col = get_vehicle_collection()
    query = {"make": {"$regex": make, "$options": "i"}} if make else {}
    cursor = col.find(query, {"min_acceptable_price": 0, "embedding": 0}).sort("year", -1).skip((page-1)*12).limit(12)
    vehicles = await cursor.to_list(length=12)
    for v in vehicles:
        v["id"] = str(v["_id"])
    return vehicles

@app.post("/search/semantic", response_model=List[VehicleSearchResponse])
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
        {"$project": {"embedding": 0, "min_acceptable_price": 0, "score": {"$meta": "vectorSearchScore"}}}
    ]
    results = await col.aggregate(pipeline).to_list(length=6)
    return [VehicleSearchResponse(id=str(r["_id"]), **r) for r in results]

@app.post("/negotiate")
async def negotiate(vehicle_id: str, offer: float, user: dict = Depends(get_current_user)):
    vehicle_col = get_vehicle_collection()
    neg_col = get_negotiations_collection()
    
    vehicle = await vehicle_col.find_one({"_id": ObjectId(vehicle_id)})
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    # Agentic Logic: Check hidden minimum price
    min_price = vehicle.get("min_acceptable_price", vehicle["price"] * 0.9)
    
    if offer >= vehicle["price"]:
        response = "That is a generous offer! We accept immediately."
        status = "accepted"
    elif offer >= min_price:
        response = f"Your offer of ${offer} is fair. We have a deal!"
        status = "accepted"
    else:
        response = f"I'm sorry, ${offer} is below the seller's minimum. Can you go higher?"
        status = "countered"

    # Persist the negotiation in Atlas
    negotiation_entry = {
        "buyer_id": user["_id"],
        "vehicle_id": vehicle_id,
        "offer_price": offer,
        "assistant_response": response,
        "status": status,
        "timestamp": datetime.utcnow()
    }
    await neg_col.insert_one(negotiation_entry)

    return {"message": response, "status": status}