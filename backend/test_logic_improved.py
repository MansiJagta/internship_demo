import asyncio
import os
from negotiator import analyze_input, logic_engine, AgentState
from langchain_core.messages import HumanMessage, AIMessage

async def test_case(name, messages, asking=40000, min_price=34000):
    print(f"\n>>> [NEW_RUN] Running Test: {name}")
    state: AgentState = {
        "messages": messages,
        "vehicle_id": "test_vid",
        "buyer_id": "test_buyer",
        "asking_price": asking,
        "min_acceptable_price": min_price,
        "offer_amount": 0.0,
        "counter_price": None,
        "decision": "PENDING"
    }
    
    # 1. Test analyze_input
    analysis = await analyze_input(state)
    state.update(analysis)
    print(f"Extracted Offer: ${state['offer_amount']}")
    
    # 2. Test logic_engine
    logic = await logic_engine(state)
    state.update(logic)
    print(f"Decision: {state['decision']}")
    if state['counter_price']:
        print(f"Counter Price: ${state['counter_price']}")

async def main():
    # Scenario 1: Basic offer
    await test_case("Simple Offer", [HumanMessage(content="I want this for 35000")])
    
    # Scenario 2: Multiple numbers (take the last one)
    await test_case("Multiple Numbers", [HumanMessage(content="I can't do 38000, but I can do 32000.")])
    
    # Scenario 3: Low-ball offer
    await test_case("Low-ball Offer", [HumanMessage(content="I'll give you $50")])
    
    # Scenario 4: Very close to asking
    await test_case("Near-Ask Offer", [HumanMessage(content="How about 39500?")])
    
    # Scenario 5: Just below min
    await test_case("Below Min", [HumanMessage(content="31000 is my max.")])

if __name__ == "__main__":
    asyncio.run(main())
