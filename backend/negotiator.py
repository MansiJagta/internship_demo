import os
import re
import uuid
from datetime import datetime
from typing import Annotated, Literal, TypedDict, List, Optional
try:
    from bson import ObjectId
except ImportError:
    from bson.objectid import ObjectId
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from database import get_vehicle_collection, get_negotiations_collection

# --- State Definition ---
def add_messages(left: list, right: list):
    return left + right

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    vehicle_id: str
    buyer_id: str
    offer_amount: float
    counter_price: Optional[float]
    min_acceptable_price: float
    asking_price: float
    decision: Literal["ACCEPT", "COUNTER", "REJECT", "PENDING"]

# --- Nodes ---

async def analyze_input(state: AgentState):
    """Extract numerical value from user text using Regex."""
    # We look at the LAST HumanMessage content
    last_user_msg = ""
    for m in reversed(state["messages"]):
        if isinstance(m, HumanMessage):
            last_user_msg = m.content
            break
            
    if not last_user_msg:
        return {"offer_amount": 0.0}

    # Robust regex to find numbers like $15,000, 15000, or 15000.50
    # We prioritize comma-separated numbers, then fall back to plain digits.
    # We look for the LAST number in the message, which is usually the offer.
    matches = re.findall(r'\$?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?', last_user_msg)
    offer = 0.0
    if matches:
        try:
            # We take the last match as the primary offer if there are multiple
            # e.g., "I can't do 30k, how about 25000" -> 25000
            last_match = matches[-1]
            num_str = last_match.replace(',', '').replace('$', '')
            offer = float(num_str)
        except (ValueError, IndexError):
            pass
    
    return {"offer_amount": offer}

async def fetch_vehicle_context(state: AgentState):
    """Context retrieval from MongoDB."""
    vehicle_col = get_vehicle_collection()
    try:
        vehicle = await vehicle_col.find_one({"_id": ObjectId(state["vehicle_id"])})
    except Exception:
        vehicle = None
        
    if not vehicle:
        return {"asking_price": 0.0, "min_acceptable_price": 0.0}
    
    asking_price = vehicle.get("price", 0.0)
    # Hidden minimum is 85% of asking if not specified
    min_price = vehicle.get("min_acceptable_price", asking_price * 0.85)
    
    return {
        "asking_price": asking_price,
        "min_acceptable_price": min_price
    }

async def logic_engine(state: AgentState):
    """Mathematical decision-making."""
    offer = state["offer_amount"]
    asking = state["asking_price"]
    min_price = state["min_acceptable_price"]
    
    if offer <= 0:
        return {"decision": "REJECT", "counter_price": None}
    
    # If the offer is ridiculously low (less than 60% of asking), it's a hard rejection
    if offer < asking * 0.6:
        return {"decision": "REJECT", "counter_price": None}

    if offer >= asking:
        decision = "ACCEPT"
        counter = None
    elif offer >= min_price:
        # If it's between min and asking, we can accept if close, or counter.
        if offer >= asking * 0.96:
            decision = "ACCEPT"
            counter = None
        else:
            decision = "COUNTER"
            # Counter logic: split the difference between current offer and asking, 
            # but stay above min_price * 1.05
            counter = round((asking + offer) / 2, -2)
            counter = max(counter, round(min_price * 1.02, -2))
    else:
        # Offer is below min_acceptable but above 60% threshold
        decision = "COUNTER"
        # Counter with something just above min_price
        counter = round(max(min_price * 1.05, (asking + min_price) / 2), -2)
        
    return {"decision": decision, "counter_price": counter}

async def formulate_response(state: AgentState):
    """Persona-based text generation."""
    decision = state["decision"]
    offer = state["offer_amount"]
    asking = state["asking_price"]
    min_price = state["min_acceptable_price"]
    counter = state.get("counter_price")
    
    # Format history for the prompt
    history_str = ""
    for m in state["messages"][:-1]:
        role = "Buyer" if isinstance(m, HumanMessage) else "Dealer"
        history_str += f"{role}: {m.content}\n"

    system_msg = (
        "You are a Professional Car Dealer at AutoVibe. Your goal is to be polite, persuasive, and professional.\n\n"
        "DATABASE CONTEXT:\n"
        f"- Asking Price: ${asking:,.0f}\n"
        f"- Current Offer: ${offer:,.0f}\n"
        f"- Decision: {decision}\n"
    )
    
    if decision == "COUNTER" and counter:
        system_msg += f"- You MUST suggest a counter-offer of EXACTLY ${counter:,.0f}.\n"
    elif decision == "REJECT":
        system_msg += "- You MUST politely reject the offer as it is too low. Do NOT suggest a lower price yet unless they come closer to $min_price.\n"
    elif decision == "ACCEPT":
        system_msg += "- You MUST accept the offer enthusiastically.\n"

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_msg + "\nCONSIDER CHAT HISTORY:\n{history}"),
        ("user", "{user_input}")
    ])
    
    # Configuration for LLM
    llm_model = os.getenv("LLM_MODEL", "llama3.1")
    llm_base_url = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
    api_key = os.getenv("OPENAI_API_KEY", "ollama")

    try:
        llm = ChatOpenAI(
            model=llm_model,
            base_url=llm_base_url,
            openai_api_key=api_key,
            temperature=0.7
        )
        chain = prompt | llm
        response = await chain.ainvoke({
            "history": history_str,
            "user_input": state["messages"][-1].content
        })
        reply = response.content
    except Exception as e:
        print(f"LLM Error: {e}. Falling back to template.")
        if decision == "ACCEPT":
            reply = f"That's a fantastic offer! We've checked the numbers, and we're happy to accept ${offer:,.0f}. Welcome to the AutoVibe family! 🎉"
        elif decision == "COUNTER" and counter:
            reply = f"I appreciate the offer of ${offer:,.0f}. While we can't quite get there, I've spoken with my manager and we can do ${counter:,.0f} today. Does that work for you?"
        else:
            # Rejection or generic counter
            suggested = round(min_price * 1.1, -2)
            reply = f"Thank you for your interest. Unfortunately, ${offer:,.0f} is a bit too far from our asking price. If you can come closer to ${suggested:,.0f}, we'd be happy to talk further."

    return {"messages": [AIMessage(content=reply)]}

    return {"messages": [AIMessage(content=reply)]}

async def persist_negotiation(state: AgentState):
    """Async upsert into MongoDB."""
    neg_col = get_negotiations_collection()
    
    # Structure the document for upsert
    # We identify a negotiation by vehicle_id and buyer_id
    query = {
        "vehicle_id": state["vehicle_id"],
        "buyer_id": ObjectId(state["buyer_id"])
    }
    
    doc = {
        "vehicle_id": state["vehicle_id"],
        "buyer_id": ObjectId(state["buyer_id"]),
        "offer_price": state["offer_amount"],
        "counter_price": state.get("counter_price"),
        "decision": state["decision"],
        "status": state["decision"].lower() if state["decision"] != "COUNTER" else "countered",
        "messages": [{"sender": m.type, "message": m.content, "timestamp": datetime.utcnow().isoformat()} for m in state["messages"]],
        "updated_at": datetime.utcnow()
    }
    
    # Async upsert
    await neg_col.update_one(query, {"$set": doc}, upsert=True)
    return state

# --- Graph ---
workflow = StateGraph(AgentState)

workflow.add_node("analyze_input", analyze_input)
workflow.add_node("fetch_vehicle_context", fetch_vehicle_context)
workflow.add_node("logic_engine", logic_engine)
workflow.add_node("formulate_response", formulate_response)
workflow.add_node("persist_negotiation", persist_negotiation)

workflow.set_entry_point("analyze_input")
workflow.add_edge("analyze_input", "fetch_vehicle_context")
workflow.add_edge("fetch_vehicle_context", "logic_engine")
workflow.add_edge("logic_engine", "formulate_response")
workflow.add_edge("formulate_response", "persist_negotiation")
workflow.add_edge("persist_negotiation", END)

negotiator_app = workflow.compile()
