# # import asyncio
# # import os
# # import random
# # from collections import defaultdict

# # from dotenv import load_dotenv
# # from faker import Faker
# # from motor.motor_asyncio import AsyncIOMotorClient
# # from sentence_transformers import SentenceTransformer

# # from database import db_helper, get_vehicle_collection
# # from models import Vehicle

# # TOTAL_VEHICLES = 50
# # EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# # MAKE_MODEL_MAP = {
# #     "Toyota": ["Camry", "Corolla", "RAV4", "Highlander"],
# #     "Honda": ["Civic", "Accord", "CR-V", "Pilot"],
# #     "Ford": ["Mustang", "Explorer", "F-150", "Escape"],
# #     "BMW": ["3 Series", "5 Series", "X3", "X5"],
# #     "Audi": ["A4", "A6", "Q5", "Q7"],
# #     "Tesla": ["Model 3", "Model Y", "Model S", "Model X"],
# #     "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe"],
# #     "Kia": ["K5", "Sportage", "Sorento", "Telluride"],
# # }


# # def generate_vehicle(fake: Faker, idx: int) -> Vehicle:
# #     make = random.choice(list(MAKE_MODEL_MAP.keys()))
# #     model = random.choice(MAKE_MODEL_MAP[make])
# #     year = random.randint(2014, 2025)

# #     age = 2026 - year
# #     mileage = max(0, int(random.gauss(max(age, 1) * 12000, 9000)))

# #     base_price = 18000 + ((year - 2014) * 1700) + random.randint(0, 22000)
# #     depreciation = mileage * random.uniform(0.03, 0.08)
# #     price = max(4500, base_price - depreciation)

# #     # Seed some aggressively discounted records so anomaly logic can detect them.
# #     if random.random() < 0.16:
# #         price *= random.uniform(0.55, 0.7)

# #     price = round(price, 2)
# #     min_acceptable_price = round(price * 0.85, 2)

# #     description = (
# #         f"{year} {make} {model} in excellent condition. "
# #         f"{fake.sentence(nb_words=12)} "
# #         f"Single-owner history, clean records, and recently serviced."
# #     )

# #     image_url = f"https://picsum.photos/seed/autovibe-{idx}/900/600"

# #     return Vehicle(
# #         make=make,
# #         model=model,
# #         year=year,
# #         price=price,
# #         mileage=mileage,
# #         description=description,
# #         image_url=image_url,
# #         min_acceptable_price=min_acceptable_price,
# #     )


# # def apply_anomaly_detection(vehicles: list[Vehicle]) -> list[Vehicle]:
# #     prices_by_year: dict[int, list[float]] = defaultdict(list)
# #     for vehicle in vehicles:
# #         prices_by_year[vehicle.year].append(vehicle.price)

# #     avg_price_by_year = {
# #         year: (sum(prices) / len(prices)) for year, prices in prices_by_year.items()
# #     }

# #     updated: list[Vehicle] = []
# #     for vehicle in vehicles:
# #         year_avg = avg_price_by_year[vehicle.year]
# #         is_suspicious = vehicle.price < (0.7 * year_avg)
# #         updated.append(vehicle.model_copy(update={"is_suspicious": is_suspicious}))

# #     return updated


# # def attach_embeddings(vehicles: list[Vehicle]) -> list[Vehicle]:
# #     print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
# #     embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)
# #     descriptions = [vehicle.description for vehicle in vehicles]

# #     embeddings = embedder.encode(
# #         descriptions,
# #         convert_to_numpy=True,
# #         show_progress_bar=False,
# #         normalize_embeddings=True,
# #     )

# #     updated: list[Vehicle] = []
# #     for idx, vehicle in enumerate(vehicles):
# #         embedding = [float(value) for value in embeddings[idx].tolist()]
# #         updated.append(vehicle.model_copy(update={"embedding": embedding}))

# #     return updated


# # async def seed_database() -> None:
# #     load_dotenv()

# #     mongodb_url = os.getenv("MONGODB_URL")
# #     if not mongodb_url:
# #         raise RuntimeError("MONGODB_URL is not configured.")

# #     fake = Faker()

# #     db_helper.client = AsyncIOMotorClient(mongodb_url)
# #     db_helper.db = db_helper.client.get_database("autovibe_db")

# #     try:
# #         await db_helper.client.admin.command("ping")
# #         print("Connected to MongoDB Atlas.")

# #         vehicles: list[Vehicle] = []
# #         for i in range(1, TOTAL_VEHICLES + 1):
# #             vehicles.append(generate_vehicle(fake, i))
# #             if i % 10 == 0:
# #                 print(f"Generated {i}/{TOTAL_VEHICLES} vehicles...")

# #         vehicles = apply_anomaly_detection(vehicles)
# #         print("Applied anomaly detection.")

# #         vehicles = attach_embeddings(vehicles)
# #         print("Generated embeddings for all vehicles.")

# #         collection = get_vehicle_collection()
# #         await collection.delete_many({})
# #         print("Cleared existing vehicles collection.")

# #         documents = [vehicle.model_dump(mode="json") for vehicle in vehicles]
# #         await collection.insert_many(documents)

# #         print("Database seeded successfully!")
# #     finally:
# #         if db_helper.client:
# #             db_helper.client.close()
# #             print("MongoDB connection closed.")


# # if __name__ == "__main__":
# #     asyncio.run(seed_database())










# # import asyncio
# # import os
# # import random
# # from collections import defaultdict

# # from dotenv import load_dotenv
# # from faker import Faker
# # from motor.motor_asyncio import AsyncIOMotorClient
# # from sentence_transformers import SentenceTransformer

# # from database import db_helper, get_vehicle_collection
# # from models import Vehicle

# # TOTAL_VEHICLES = 50
# # EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# # MAKE_MODEL_MAP = {
# #     "Toyota": ["Camry", "Corolla", "RAV4", "Highlander"],
# #     "Honda": ["Civic", "Accord", "CR-V", "Pilot"],
# #     "Ford": ["Mustang", "Explorer", "F-150", "Escape"],
# #     "BMW": ["3 Series", "5 Series", "X3", "X5"],
# #     "Audi": ["A4", "A6", "Q5", "Q7"],
# #     "Tesla": ["Model 3", "Model Y", "Model S", "Model X"],
# #     "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe"],
# #     "Kia": ["K5", "Sportage", "Sorento", "Telluride"],
# # }


# # def generate_vehicle(fake: Faker, idx: int) -> Vehicle:
# #     make = random.choice(list(MAKE_MODEL_MAP.keys()))
# #     model = random.choice(MAKE_MODEL_MAP[make])
# #     year = random.randint(2014, 2025)

# #     age = 2026 - year
# #     mileage = max(0, int(random.gauss(max(age, 1) * 12000, 9000)))

# #     base_price = 18000 + ((year - 2014) * 1700) + random.randint(0, 22000)
# #     depreciation = mileage * random.uniform(0.03, 0.08)
# #     price = max(4500, base_price - depreciation)

# #     # Seed some aggressively discounted records so anomaly logic can detect them.
# #     if random.random() < 0.16:
# #         price *= random.uniform(0.55, 0.7)

# #     price = round(price, 2)
# #     min_acceptable_price = round(price * 0.85, 2)

# #     description = (
# #         f"{year} {make} {model} in excellent condition. "
# #         f"{fake.sentence(nb_words=12)} "
# #         f"Single-owner history, clean records, and recently serviced."
# #     )

# #     image_url = f"https://picsum.photos/seed/autovibe-{idx}/900/600"

# #     return Vehicle(
# #         make=make,
# #         model=model,
# #         year=year,
# #         price=price,
# #         mileage=mileage,
# #         description=description,
# #         image_url=image_url,
# #         min_acceptable_price=min_acceptable_price,
# #     )


# # def apply_anomaly_detection(vehicles: list[Vehicle]) -> list[Vehicle]:
# #     prices_by_year: dict[int, list[float]] = defaultdict(list)
# #     for vehicle in vehicles:
# #         prices_by_year[vehicle.year].append(vehicle.price)

# #     avg_price_by_year = {
# #         year: (sum(prices) / len(prices)) for year, prices in prices_by_year.items()
# #     }

# #     updated: list[Vehicle] = []
# #     for vehicle in vehicles:
# #         year_avg = avg_price_by_year[vehicle.year]
# #         is_suspicious = vehicle.price < (0.7 * year_avg)
# #         updated.append(vehicle.model_copy(update={"is_suspicious": is_suspicious}))

# #     return updated


# # def attach_embeddings(vehicles: list[Vehicle]) -> list[Vehicle]:
# #     print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
# #     embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)
# #     descriptions = [vehicle.description for vehicle in vehicles]

# #     embeddings = embedder.encode(
# #         descriptions,
# #         convert_to_numpy=True,
# #         show_progress_bar=False,
# #         normalize_embeddings=True,
# #     )

# #     updated: list[Vehicle] = []
# #     for idx, vehicle in enumerate(vehicles):
# #         embedding = [float(value) for value in embeddings[idx].tolist()]
# #         updated.append(vehicle.model_copy(update={"embedding": embedding}))

# #     return updated


# # async def seed_database() -> None:
# #     load_dotenv()

# #     mongodb_url = os.getenv("MONGODB_URL")
# #     if not mongodb_url:
# #         raise RuntimeError("MONGODB_URL is not configured.")

# #     fake = Faker()

# #     db_helper.client = AsyncIOMotorClient(mongodb_url)
# #     db_helper.db = db_helper.client.get_database("autovibe_db")

# #     try:
# #         await db_helper.client.admin.command("ping")
# #         print("Connected to MongoDB Atlas.")

# #         vehicles: list[Vehicle] = []
# #         for i in range(1, TOTAL_VEHICLES + 1):
# #             vehicles.append(generate_vehicle(fake, i))
# #             if i % 10 == 0:
# #                 print(f"Generated {i}/{TOTAL_VEHICLES} vehicles...")

# #         vehicles = apply_anomaly_detection(vehicles)
# #         print("Applied anomaly detection.")

# #         vehicles = attach_embeddings(vehicles)
# #         print("Generated embeddings for all vehicles.")

# #         collection = get_vehicle_collection()
# #         await collection.delete_many({})
# #         print("Cleared existing vehicles collection.")

# #         documents = [vehicle.model_dump(mode="json") for vehicle in vehicles]
# #         await collection.insert_many(documents)

# #         print("Database seeded successfully!")
# #     finally:
# #         if db_helper.client:
# #             db_helper.client.close()
# #             print("MongoDB connection closed.")


# # if __name__ == "__main__":
# #     asyncio.run(seed_database())













# import asyncio
# import os
# import random
# from collections import defaultdict
# from datetime import datetime

# from dotenv import load_dotenv
# from faker import Faker
# from motor.motor_asyncio import AsyncIOMotorClient
# from passlib.context import CryptContext
# from sentence_transformers import SentenceTransformer
# from bson import ObjectId

# from database import db_helper, get_vehicle_collection, get_user_collection, get_negotiations_collection
# from models import Vehicle

# TOTAL_VEHICLES = 50
# EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MAKE_MODEL_MAP = {
#     "Toyota": ["Camry", "Corolla", "RAV4", "Highlander"],
#     "Honda": ["Civic", "Accord", "CR-V", "Pilot"],
#     "Ford": ["Mustang", "Explorer", "F-150", "Escape"],
#     "BMW": ["3 Series", "5 Series", "X3", "X5"],
#     "Audi": ["A4", "A6", "Q5", "Q7"],
#     "Tesla": ["Model 3", "Model Y", "Model S", "Model X"],
#     "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe"],
#     "Kia": ["K5", "Sportage", "Sorento", "Telluride"],
# }


# def generate_vehicle(fake: Faker, idx: int) -> Vehicle:
#     make = random.choice(list(MAKE_MODEL_MAP.keys()))
#     model = random.choice(MAKE_MODEL_MAP[make])
#     year = random.randint(2014, 2025)

#     age = 2026 - year
#     mileage = max(0, int(random.gauss(max(age, 1) * 12000, 9000)))

#     base_price = 18000 + ((year - 2014) * 1700) + random.randint(0, 22000)
#     depreciation = mileage * random.uniform(0.03, 0.08)
#     price = max(4500, base_price - depreciation)

#     # Seed some aggressively discounted records so anomaly logic can detect them.
#     if random.random() < 0.16:
#         price *= random.uniform(0.55, 0.7)

#     price = round(price, 2)
#     min_acceptable_price = round(price * 0.85, 2)

#     description = (
#         f"{year} {make} {model} in excellent condition. "
#         f"{fake.sentence(nb_words=12)} "
#         f"Single-owner history, clean records, and recently serviced."
#     )

#     image_url = f"https://picsum.photos/seed/autovibe-{idx}/900/600"

#     return Vehicle(
#         make=make,
#         model=model,
#         year=year,
#         price=price,
#         mileage=mileage,
#         description=description,
#         image_url=image_url,
#         min_acceptable_price=min_acceptable_price,
#     )


# def apply_anomaly_detection(vehicles: list[Vehicle]) -> list[Vehicle]:
#     prices_by_year: dict[int, list[float]] = defaultdict(list)
#     for vehicle in vehicles:
#         prices_by_year[vehicle.year].append(vehicle.price)

#     avg_price_by_year = {
#         year: (sum(prices) / len(prices)) for year, prices in prices_by_year.items()
#     }

#     updated: list[Vehicle] = []
#     for vehicle in vehicles:
#         year_avg = avg_price_by_year[vehicle.year]
#         is_suspicious = vehicle.price < (0.7 * year_avg)
#         updated.append(vehicle.model_copy(update={"is_suspicious": is_suspicious}))

#     return updated


# def attach_embeddings(vehicles: list[Vehicle]) -> list[Vehicle]:
#     print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
#     embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)
#     descriptions = [vehicle.description for vehicle in vehicles]

#     embeddings = embedder.encode(
#         descriptions,
#         convert_to_numpy=True,
#         show_progress_bar=False,
#         normalize_embeddings=True,
#     )

#     updated: list[Vehicle] = []
#     for idx, vehicle in enumerate(vehicles):
#         embedding = [float(value) for value in embeddings[idx].tolist()]
#         updated.append(vehicle.model_copy(update={"embedding": embedding}))

#     return updated


# async def seed_users() -> dict:
#     """Seed user collection with test accounts."""
#     users_col = get_user_collection()

#     # Clear existing users
#     await users_col.delete_many({})
#     print("✓ Cleared users collection")

#     users_data = [
#         {
#             "name": "Admin User",
#             "email": "admin@example.com",
#             "password": pwd_context.hash("Admin@123"),
#             "role": "admin",
#             "is_active": True,
#             "created_at": datetime.utcnow(),
#         },
#         {
#             "name": "Seller User",
#             "email": "seller@example.com",
#             "password": pwd_context.hash("Seller@123"),
#             "role": "seller",
#             "is_active": True,
#             "created_at": datetime.utcnow(),
#         },
#         {
#             "name": "Buyer User",
#             "email": "buyer@example.com",
#             "password": pwd_context.hash("Buyer@123"),
#             "role": "buyer",
#             "is_active": True,
#             "created_at": datetime.utcnow(),
#         },
#         {
#             "name": "John Buyer",
#             "email": "john@example.com",
#             "password": pwd_context.hash("John@123"),
#             "role": "buyer",
#             "is_active": True,
#             "created_at": datetime.utcnow(),
#         },
#         {
#             "name": "Mary Seller",
#             "email": "mary@example.com",
#             "password": pwd_context.hash("Mary@123"),
#             "role": "seller",
#             "is_active": True,
#             "created_at": datetime.utcnow(),
#         },
#     ]

#     result = await users_col.insert_many(users_data)
#     await users_col.create_index("email", unique=True)

#     print(f"✓ Seeded {len(result.inserted_ids)} users")

#     return {
#         "admin_id": str(result.inserted_ids[0]),
#         "seller_id": str(result.inserted_ids[1]),
#         "buyer_id": str(result.inserted_ids[2]),
#         "john_id": str(result.inserted_ids[3]),
#         "mary_id": str(result.inserted_ids[4]),
#     }


# async def seed_vehicles() -> list[str]:
#     """Seed vehicle collection with 50 cars and embeddings."""
#     collection = get_vehicle_collection()

#     # Clear existing vehicles
#     await collection.delete_many({})
#     print("✓ Cleared vehicles collection")

#     fake = Faker()

#     vehicles: list[Vehicle] = []
#     for i in range(1, TOTAL_VEHICLES + 1):
#         vehicles.append(generate_vehicle(fake, i))
#         if i % 10 == 0:
#             print(f"  Generated {i}/{TOTAL_VEHICLES} vehicles...")

#     vehicles = apply_anomaly_detection(vehicles)
#     print("✓ Applied anomaly detection")

#     vehicles = attach_embeddings(vehicles)
#     print("✓ Generated embeddings for all vehicles")

#     documents = [vehicle.model_dump(mode="json") for vehicle in vehicles]
#     result = await collection.insert_many(documents)

#     await collection.create_index("make")
#     await collection.create_index("year")
#     await collection.create_index("price")

#     print(f"✓ Seeded {len(result.inserted_ids)} vehicles")

#     return [str(vid) for vid in result.inserted_ids]


# async def seed_negotiations(user_ids: dict, vehicle_ids: list[str]) -> None:
#     """Seed sample negotiations."""
#     negotiations_col = get_negotiations_collection()

#     # Clear existing negotiations
#     await negotiations_col.delete_many({})
#     print("✓ Cleared negotiations collection")

#     negotiations_data = [
#         {
#             "buyer_id": ObjectId(user_ids["buyer_id"]),
#             "vehicle_id": vehicle_ids[0],
#             "status": "pending",
#             "initial_offer": 15000,
#             "chat_history": [
#                 {
#                     "role": "buyer",
#                     "message": "Is this vehicle still available?",
#                     "offer_price": 15000,
#                     "timestamp": datetime.utcnow(),
#                 },
#                 {
#                     "role": "assistant",
#                     "message": "I've received your offer of $15000.00. Let me check with the owner.",
#                     "timestamp": datetime.utcnow(),
#                 },
#             ],
#             "created_at": datetime.utcnow(),
#             "updated_at": datetime.utcnow(),
#         },
#         {
#             "buyer_id": ObjectId(user_ids["john_id"]),
#             "vehicle_id": vehicle_ids[1],
#             "status": "pending",
#             "initial_offer": 22500,
#             "chat_history": [
#                 {
#                     "role": "buyer",
#                     "message": "What's the lowest you can go?",
#                     "offer_price": 22500,
#                     "timestamp": datetime.utcnow(),
#                 },
#                 {
#                     "role": "assistant",
#                     "message": "I've received your offer of $22500.00. Let me check with the owner.",
#                     "timestamp": datetime.utcnow(),
#                 },
#                 {
#                     "role": "buyer",
#                     "message": "Can you do 21000?",
#                     "offer_price": 21000,
#                     "timestamp": datetime.utcnow(),
#                 },
#                 {
#                     "role": "assistant",
#                     "message": "I've received your offer of $21000.00. Let me check with the owner.",
#                     "timestamp": datetime.utcnow(),
#                 },
#             ],
#             "created_at": datetime.utcnow(),
#             "updated_at": datetime.utcnow(),
#         },
#     ]

#     result = await negotiations_col.insert_many(negotiations_data)
#     await negotiations_col.create_index([("buyer_id", 1), ("vehicle_id", 1)])

#     print(f"✓ Seeded {len(result.inserted_ids)} sample negotiations")


# async def seed_database() -> None:
#     load_dotenv()

#     mongodb_url = os.getenv("MONGODB_URL")
#     db_name = os.getenv("MONGODB_DB", "auth")
    
#     if not mongodb_url:
#         raise RuntimeError("MONGODB_URL is not configured.")

#     db_helper.client = AsyncIOMotorClient(mongodb_url)
#     db_helper.db = db_helper.client.get_database(db_name)

#     try:
#         await db_helper.client.admin.command("ping")
#         print(f"✓ Connected to MongoDB Atlas - Database: {db_name}\n")

#         print("=== SEEDING USERS ===")
#         user_ids = await seed_users()

#         print("\n=== SEEDING VEHICLES ===")
#         vehicle_ids = await seed_vehicles()

#         print("\n=== SEEDING NEGOTIATIONS ===")
#         await seed_negotiations(user_ids, vehicle_ids)

#         print("\n" + "=" * 50)
#         print("✓ DATABASE SEED COMPLETE")
#         print("=" * 50)

#         print("\n📧 TEST ACCOUNTS:")
#         print("  Admin   | admin@example.com   | Admin@123")
#         print("  Seller  | seller@example.com  | Seller@123")
#         print("  Buyer   | buyer@example.com   | Buyer@123")
#         print("  John    | john@example.com    | John@123")
#         print("  Mary    | mary@example.com    | Mary@123")

#         print(f"\n📊 SEEDED DATA:")
#         print(f"  Users: 5")
#         print(f"  Vehicles: {TOTAL_VEHICLES}")
#         print(f"  Negotiations: 2 (sample)")

#         print(f"\n📍 Database: {db_name}")

#     except Exception as e:
#         print(f"❌ Seeding failed: {str(e)}")
#         raise
#     finally:
#         if db_helper.client:
#             db_helper.client.close()
#             print("\n✓ MongoDB connection closed")


# if __name__ == "__main__":
#     asyncio.run(seed_database())


import bcrypt
import asyncio
import os
import random
from collections import defaultdict
from datetime import datetime

from dotenv import load_dotenv
from faker import Faker
from motor.motor_asyncio import AsyncIOMotorClient
from sentence_transformers import SentenceTransformer
from bson import ObjectId

# Import helpers from your existing database and models files
from database import db_helper, get_vehicle_collection, get_user_collection, get_negotiations_collection
from models import Vehicle

# Configuration
TOTAL_VEHICLES = 50
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

def hash_password(plain: str) -> str:
    """Hash a password using bcrypt directly (avoids passlib/Python 3.13 issues)."""
    return bcrypt.hashpw(plain[:72].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

MAKE_MODEL_MAP = {
    "Toyota": ["Camry", "Corolla", "RAV4", "Highlander"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot"],
    "Ford": ["Mustang", "Explorer", "F-150", "Escape"],
    "BMW": ["3 Series", "5 Series", "X3", "X5"],
    "Audi": ["A4", "A6", "Q5", "Q7"],
    "Tesla": ["Model 3", "Model Y", "Model S", "Model X"],
    "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe"],
    "Kia": ["K5", "Sportage", "Sorento", "Telluride"],
}

FUEL_TYPES = ["Gasoline", "Electric", "Hybrid", "Diesel"]
TRANSMISSIONS = ["Automatic", "Manual", "CVT", "DCT", "Single-Speed"]
DRIVETRAINS = ["FWD", "RWD", "AWD", "4WD"]
COLORS_EXT = ["Pearl White", "Midnight Black", "Deep Blue", "Racing Red", "Forest Green",
              "Silver", "Champagne Gold", "Slate Gray", "Navy Blue", "Burnt Orange"]
COLORS_INT = ["Black", "Cognac", "Gray", "Cream", "Red Pepper", "Brown", "Beige", "White"]
LOCATIONS = ["San Francisco, CA", "Los Angeles, CA", "New York, NY", "Miami, FL",
             "Chicago, IL", "Seattle, WA", "Austin, TX", "Denver, CO", "Phoenix, AZ", "Detroit, MI"]

MAKE_SPECS = {
    "Toyota":  {"fuel": ["Gasoline", "Hybrid"], "hp_range": (170, 302), "mpg_city": (28, 40), "mpg_hwy": (35, 50)},
    "Honda":   {"fuel": ["Gasoline", "Hybrid"], "hp_range": (158, 315), "mpg_city": (28, 40), "mpg_hwy": (34, 48)},
    "Ford":    {"fuel": ["Gasoline", "Electric"], "hp_range": (180, 486), "mpg_city": (15, 30), "mpg_hwy": (22, 38)},
    "BMW":     {"fuel": ["Gasoline", "Hybrid"], "hp_range": (255, 617), "mpg_city": (16, 28), "mpg_hwy": (24, 36)},
    "Audi":    {"fuel": ["Gasoline", "Electric"], "hp_range": (201, 637), "mpg_city": (19, 79), "mpg_hwy": (27, 82)},
    "Tesla":   {"fuel": ["Electric"],             "hp_range": (283, 1020),"mpg_city": (100, 135),"mpg_hwy": (100, 130)},
    "Hyundai": {"fuel": ["Gasoline", "Electric", "Hybrid"], "hp_range": (147, 483), "mpg_city": (25, 115), "mpg_hwy": (32, 120)},
    "Kia":     {"fuel": ["Gasoline", "Electric", "Hybrid"], "hp_range": (147, 320), "mpg_city": (26, 120), "mpg_hwy": (33, 115)},
}

def generate_vin(fake: "Faker", make: str, idx: int) -> str:
    prefix = make[:2].upper()
    return f"{prefix}A{fake.bothify('??####??###')}{idx:04d}"[-17:]

def generate_vehicle(fake: "Faker", idx: int) -> "Vehicle":
    make = random.choice(list(MAKE_MODEL_MAP.keys()))
    model = random.choice(MAKE_MODEL_MAP[make])
    year = random.randint(2014, 2025)

    age = 2026 - year
    mileage = max(0, int(random.gauss(max(age, 1) * 12000, 9000)))

    base_price = 18000 + ((year - 2014) * 1700) + random.randint(0, 22000)
    depreciation = mileage * random.uniform(0.03, 0.08)
    price = max(4500, base_price - depreciation)

    # Inject Anomaly: Seed some aggressively discounted records (Option A: Anomaly Detection)
    if random.random() < 0.16:
        price *= random.uniform(0.55, 0.7)

    price = round(price, 2)
    min_acceptable_price = round(price * 0.85, 2)

    description = (
        f"{year} {make} {model} in excellent condition. "
        f"{fake.sentence(nb_words=12)} "
        f"Single-owner history, clean records, and recently serviced."
    )

    # Rich spec fields
    specs = MAKE_SPECS.get(make, {"fuel": ["Gasoline"], "hp_range": (150, 300), "mpg_city": (18, 28), "mpg_hwy": (25, 35)})
    fuel_type = random.choice(specs["fuel"])
    transmission = "Single-Speed" if fuel_type == "Electric" else random.choice(["Automatic", "DCT", "Manual", "CVT"])
    horsepower = random.randint(*specs["hp_range"])
    drivetrain = random.choice(DRIVETRAINS)
    mpg_city = random.randint(*specs["mpg_city"])
    mpg_highway = random.randint(*specs["mpg_hwy"])
    ext_color = random.choice(COLORS_EXT)
    int_color = random.choice(COLORS_INT)
    location = random.choice(LOCATIONS)
    listed_date = fake.date_between(start_date="-60d", end_date="today").strftime("%Y-%m-%d")
    vin = generate_vin(fake, make, idx)
    engine_size = round(random.uniform(1.5, 5.0), 1)
    engine = f"Electric Motor" if fuel_type == "Electric" else f"{engine_size}L {random.choice(['I4','V6','V8','I6','Flat-6'])}"
    seller = random.choice(["AutoVibe Certified", "Private Seller", f"{make} Dealer", "Exotic Motors"])

    # Generate multiple image URLs (using picsum seeds for variety)
    base_img = f"https://picsum.photos/seed/autovibe-{idx}/900/600"
    images = [
        f"https://picsum.photos/seed/autovibe-{idx}/900/600",
        f"https://picsum.photos/seed/autovibe-{idx}-2/900/600",
        f"https://picsum.photos/seed/autovibe-{idx}-3/900/600",
    ]

    return Vehicle(
        make=make,
        model=model,
        year=year,
        price=price,
        mileage=mileage,
        description=description,
        image_url=base_img,
        images=images,
        fuel_type=fuel_type,
        transmission=transmission,
        engine=engine,
        horsepower=horsepower,
        drivetrain=drivetrain,
        exterior_color=ext_color,
        interior_color=int_color,
        mpg_city=mpg_city,
        mpg_highway=mpg_highway,
        seller=seller,
        location=location,
        listed_date=listed_date,
        vin=vin,
        min_acceptable_price=min_acceptable_price,
    )

def apply_anomaly_detection(vehicles: list[Vehicle]) -> list[Vehicle]:
    """Flag vehicles priced significantly below the market average for their year."""
    prices_by_year: dict[int, list[float]] = defaultdict(list)
    for vehicle in vehicles:
        prices_by_year[vehicle.year].append(vehicle.price)

    avg_price_by_year = {
        year: (sum(prices) / len(prices)) for year, prices in prices_by_year.items()
    }

    updated: list[Vehicle] = []
    for vehicle in vehicles:
        year_avg = avg_price_by_year[vehicle.year]
        # Anomaly logic: price < 70% of yearly average
        is_suspicious = vehicle.price < (0.7 * year_avg)
        updated.append(vehicle.model_copy(update={"is_suspicious": is_suspicious}))

    return updated

def attach_embeddings(vehicles: list[Vehicle]) -> list[Vehicle]:
    """Generate vectors for Semantic Search (Option B: Semantic Search)."""
    print(f"🧠 Loading AI Model: {EMBEDDING_MODEL_NAME}...")
    embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)
    descriptions = [vehicle.description for vehicle in vehicles]

    embeddings = embedder.encode(
        descriptions,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    updated: list[Vehicle] = []
    for idx, vehicle in enumerate(vehicles):
        embedding = [float(value) for value in embeddings[idx].tolist()]
        updated.append(vehicle.model_copy(update={"embedding": embedding}))

    return updated

async def seed_users() -> dict:
    """Seed user collection with persistent test accounts for your demo."""
    users_col = get_user_collection()
    await users_col.delete_many({})
    print("✓ Cleared users collection")

    users_data = [
        {"name": "Mansi Jagtap", "email": "mansi@example.com", "password": hash_password("password123"), "role": "buyer", "created_at": datetime.utcnow()},
        {"name": "Admin User", "email": "admin@example.com", "password": hash_password("Admin@123"), "role": "admin", "created_at": datetime.utcnow()},
        {"name": "Seller User", "email": "seller@example.com", "password": hash_password("Seller@123"), "role": "seller", "created_at": datetime.utcnow()},
    ]

    result = await users_col.insert_many(users_data)
    await users_col.create_index("email", unique=True)
    print(f"✓ Seeded {len(result.inserted_ids)} users")

    return {
        "mansi_id": str(result.inserted_ids[0]),
        "admin_id": str(result.inserted_ids[1]),
        "seller_id": str(result.inserted_ids[2]),
    }

async def seed_database() -> None:
    load_dotenv()
    mongodb_url = os.getenv("MONGODB_URL")
    
    if not mongodb_url:
        raise RuntimeError("MONGODB_URL is not configured in .env")

    db_helper.client = AsyncIOMotorClient(mongodb_url)
    db_helper.db = db_helper.client.get_database("autovibe_db")

    try:
        await db_helper.client.admin.command("ping")
        print("🚀 Connected to MongoDB Atlas.")

        # 1. Seed Users
        print("\n=== SEEDING USERS ===")
        user_ids = await seed_users()

        # 2. Generate Vehicles
        print("\n=== GENERATING VEHICLES ===")
        fake = Faker()
        raw_vehicles = [generate_vehicle(fake, i) for i in range(1, TOTAL_VEHICLES + 1)]
        
        # 3. Apply AI Logic (Anomaly + Embeddings)
        vehicles_with_anomalies = apply_anomaly_detection(raw_vehicles)
        final_vehicles = attach_embeddings(vehicles_with_anomalies)

        # 4. Upload to Atlas
        collection = get_vehicle_collection()
        await collection.delete_many({})
        docs = [v.model_dump(mode="json") for v in final_vehicles]
        result = await collection.insert_many(docs)
        
        # Create standard indexes for filtering performance
        await collection.create_index("make")
        await collection.create_index("price")
        
        print(f"✅ Database seeded with {len(result.inserted_ids)} vehicles and AI embeddings!")
        print("\n📍 TEST CREDENTIALS:")
        print("   Email: mansi@example.com | Password: password123")

    except Exception as e:
        print(f"❌ Seeding failed: {str(e)}")
    finally:
        if db_helper.client:
            db_helper.client.close()
            print("\n✓ MongoDB connection closed")

if __name__ == "__main__":
    asyncio.run(seed_database())