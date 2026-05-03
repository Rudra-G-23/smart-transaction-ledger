import os
import pandas as pd
import requests
from io import StringIO
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Dataset Chatbot")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# CSV URLs
FRAUD_URL = "https://raw.githubusercontent.com/Rudra-G-23/smart-transaction-ledger/main/data/gold/gold_fraud_dataset.csv"
MERCHANT_URL = "https://raw.githubusercontent.com/Rudra-G-23/smart-transaction-ledger/main/data/gold/gold_merchant_risk.csv"
USER_URL = "https://raw.githubusercontent.com/Rudra-G-23/smart-transaction-ledger/main/data/gold/gold_user_behavior.csv"

def load_csv(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text))
    except:
        return pd.DataFrame()

# Load dataframes globally
fraud_df = load_csv(FRAUD_URL)
merchant_df = load_csv(MERCHANT_URL)
user_df = load_csv(USER_URL)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.get("/")
async def root():
    return {
        "status": "Dataset Chatbot ready",
        "datasets": {
            "fraud": {"rows": len(fraud_df)},
            "merchant": {"rows": len(merchant_df)},
            "user_behavior": {"rows": len(user_df)}
        }
    }

@app.post("/chat")
async def chat(request: dict):  # ✅ dict, not BaseModel - accepts "question" OR "message"
    user_question = request.get("question") or request.get("message", "")
    if not user_question:
        return {"error": "No question provided"}

    # Context: dataset info + question
    context = f"""
Gold transaction datasets loaded:
- fraud: {len(fraud_df)} rows
- merchant: {len(merchant_df)} rows  
- user_behavior: {len(user_df)} rows

Question: {user_question}
Answer using dataset statistics, patterns, top values. Suggest pandas queries for deeper analysis.
"""

    messages = [
        {"role": "system", "content": "Gold fraud data analyst. Use dataset row counts and typical fraud analysis patterns. Be specific about merchants, amounts, risk scores."},
        {"role": "user", "content": context}
    ]

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ Free/working model May 2026
            messages=messages,
            temperature=0.1,
            max_tokens=400
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        return {"error": f"API Error: {str(e)}"}