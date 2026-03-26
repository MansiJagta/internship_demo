# AutoVibe: Smart AI-Driven Vehicle Marketplace

**AutoVibe** is a high-performance, AI-native backend engine designed for a modern vehicle marketplace. It integrates **Semantic Search**, **Statistical Anomaly Detection**, and an **Agentic Price Negotiator** powered by a stateful LangGraph workflow and a local Llama 3.1 model.

---

## 🌟 Key Features

* **Agentic Price Negotiator:** A multi-turn AI "Seller" that uses **LangGraph** to handle price bargaining while protecting hidden profit margins.
* **Semantic Search:** Natural language search powered by **SentenceTransformers** and **MongoDB Atlas Vector Search** (e.g., "A spacious SUV for a family under 20k").
* **Anomaly Detection:** Statistical guardrails that automatically flag "Suspicious Listings" (prices > 2 standard deviations below the market mean).
* **Privacy-First AI:** All LLM processing is handled locally via **Ollama (Llama 3.1)**, ensuring sensitive pricing data never leaves the server.
* **Robust Backend:** Built with **FastAPI (Python 3.13)**, utilizing asynchronous database operations with MongoDB Motor.

---

## 🏗️ Technical Architecture

### Tech Stack
* **Backend:** FastAPI (Python 3.13)
* **Database:** MongoDB Atlas (NoSQL + Vector Search)
* **AI Orchestration:** LangGraph (StateGraph)
* **LLM:** Ollama (Llama 3.1:8b)
* **Embeddings:** SentenceTransformers (`all-MiniLM-L6-v2`)
* **Security:** Passlib (PBKDF2) with Python 3.13 compatibility patches.



---

## 🚀 Local Setup & Installation

Follow these steps to get the AutoVibe engine running on your local machine.

### 1. Prerequisites
* **Python 3.13+** installed.
* **Ollama** installed ([Download here](https://ollama.com)).
* **MongoDB Atlas** account (or a local MongoDB instance).

### 2. Clone the Repository
```bash
git clone [https://github.com/MansiJagta/AutoVibe.git](https://github.com/MansiJagta/AutoVibe.git)
cd AutoVibe
3. Setup Local AI (Ollama)
Ensure the Ollama service is running, then pull the required model:

Bash

ollama pull llama3.1
4. Environment Configuration
Create a .env file in the root directory and add your credentials:

Code snippet

MONGO_URI=your_mongodb_atlas_connection_string
DATABASE_NAME=autovibe_db
# No OpenAI/Google API keys required - running fully local
5. Install Dependencies
Bash

pip install -r requirements.txt
6. Seed the Database
Run the ingestion script to populate 50+ realistic vehicle listings, calculate statistical anomalies, and generate vector embeddings:

Bash

python seed.py
7. Run the Application
Start the FastAPI server:

Bash

fastapi dev main.py
The API will be available at http://localhost:8000. Access the interactive documentation at /docs.

🛠️ API Usage & Features
1. Agentic Negotiator
Endpoint: POST /negotiate

Uses a state machine to manage the bargaining process.

Example Request:

JSON

{
  "vehicle_id": "65af...",
  "message": "I really like this car. Would you take $18,000 for it?"
}
2. Semantic Search
Endpoint: POST /search/semantic

Example Request:

JSON

{
  "query": "A reliable SUV for long trips under $30k"
}
