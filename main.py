import os
import pandas as pd
import sqlite3
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Global database connection
conn = sqlite3.connect(':memory:', check_same_thread=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load CSVs
    urls = {
        "fraud": "https://raw.githubusercontent.com/Rudra-G-23/smart-transaction-ledger/main/data/gold/gold_fraud_dataset.csv",
        "merchant": "https://raw.githubusercontent.com/Rudra-G-23/smart-transaction-ledger/main/data/gold/gold_merchant_risk.csv",
        "user": "https://raw.githubusercontent.com/Rudra-G-23/smart-transaction-ledger/main/data/gold/gold_user_behavior.csv"
    }
    for table_name, url in urls.items():
        pd.read_csv(url).to_sql(table_name, conn, index=False, if_exists='replace')
    yield
    # Shutdown: Close connection
    conn.close()

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def root():
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)['name'].tolist()
    return {"status": "DB ready", "tables": tables}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        schema = pd.read_sql("SELECT sql FROM sqlite_master WHERE type='table';", conn)['sql'].str.cat(sep='\n')
        prompt = f"Based on schema: {schema}\nGenerate ONLY valid SQLite SQL for: {request.question}\nReturn ONLY the SQL query."
        
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        sql_query = response.choices[0].message.content.strip()
        result_df = pd.read_sql(sql_query, conn)
        
        # Add summary logic here...
        return {"response": result_df.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))