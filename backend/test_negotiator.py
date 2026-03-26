import asyncio
import os
from negotiator import negotiator_app
from langchain_core.messages import HumanMessage

async def test_negotiation(vehicle_id: str, message: str, offer: float):
    print(f"\n--- Testing Negotiation: {message} (${offer}) ---")
    initial_state = {
        "messages": [HumanMessage(content=message)],
        "vehicle_id": vehicle_id,
        "offer_amount": offer,
        "decision": "PENDING"
    }
    
    try:
        final_state = await negotiator_app.ainvoke(initial_state)
        print(f"Decision: {final_state['decision']}")
        print(f"Offer: ${final_state['offer_amount']}")
        print(f"Asking: ${final_state['asking_price']}")
        print(f"Min Acceptable: ${final_state['min_acceptable_price']}")
        print(f"AI Reply: {final_state['messages'][-1].content}")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    # Manually initialize the DB connection for the test script
    from database import db_helper, get_vehicle_collection
    import os
    from motor.motor_asyncio import AsyncIOMotorClient
    
    mongodb_url = os.getenv("MONGODB_URL")
    db_helper.client = AsyncIOMotorClient(mongodb_url)
    db_helper.db = db_helper.client.get_database("autovibe_db")
    
    col = get_vehicle_collection()
    vehicle = await col.find_one({})
    if not vehicle:
        print("No vehicles found in DB, please seed first.")
        return
    
    vid = str(vehicle["_id"])
    asking = vehicle["price"]
    
    # Test 1: Offer above asking
    await test_negotiation(vid, f"I'll take it for ${asking + 1000}", asking + 1000)
    
    # Test 2: Lowball offer
    await test_negotiation(vid, "Best I can do is $100", 100)
    
    # Test 3: Realistic offer (if we can guess the min)
    await test_negotiation(vid, f"How about ${asking * 0.9}?", asking * 0.9)

if __name__ == "__main__":
    asyncio.run(main())
