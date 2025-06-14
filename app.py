# app.py
import os
import json
import sqlite3
import numpy as np
import re
from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import aiohttp
import asyncio
import logging
import base64
from fastapi.responses import JSONResponse
import uvicorn
import traceback
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
DB_PATH = "knowledge_base.db"
SIMILARITY_THRESHOLD = 0.68  # Lowered threshold for better recall
MAX_RESULTS = 10  # Increased to get more context
load_dotenv()
MAX_CONTEXT_CHUNKS = 4  # Increased number of chunks per source
API_KEY = os.getenv("API_KEY")  # Get API key from environment variable


# Models
class QueryRequest(BaseModel):
    question: str
    image: Optional[str] = None  # Base64 encoded image


class LinkInfo(BaseModel):
    url: str
    text: str


class QueryResponse(BaseModel):
    answer: str
    links: List[LinkInfo]


# Initialize FastAPI app
app = FastAPI(
    title="RAG Query API", description="API for querying the RAG knowledge base"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Verify API key is set
if not API_KEY:
    logger.error(
        "API_KEY environment variable is not set. The application will not function correctly."
    )


# Create a connection to the SQLite database
def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    except sqlite3.Error as e:
        error_msg = f"Database connection error: {e}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_msg)


# Ensure database and tables exist
if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS discourse_chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER,
        topic_id INTEGER,
        topic_title TEXT,
        post_number INTEGER,
        author TEXT,
        created_at TEXT,
        likes INTEGER,
        chunk_index INTEGER,
        content TEXT,
        url TEXT,
        embedding BLOB
    )
    """
    )
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS markdown_chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_title TEXT,
        original_url TEXT,
        downloaded_at TEXT,
        chunk_index INTEGER,
        content TEXT,
        embedding BLOB
    )
    """
    )
    conn.commit()
    conn.close()


# Cosine similarity
def cosine_similarity(vec1, vec2):
    vec1, vec2 = np.array(vec1), np.array(vec2)
    if np.all(vec1 == 0) or np.all(vec2 == 0):
        return 0.0
    dot = np.dot(vec1, vec2)
    norm1, norm2 = np.linalg.norm(vec1), np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


# (Remaining functions: get_embedding, find_similar_content, enrich_with_adjacent_chunks,
# generate_answer, process_multimodal_query, parse_llm_response)
# ...


@app.post("/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    # Implementation as per demo
    pass  # TODO: wire into functions above


@app.get("/health")
async def health_check():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM discourse_chunks")
        disc_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM markdown_chunks")
        md_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM discourse_chunks WHERE embedding IS NOT NULL")
        emb_disc = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM markdown_chunks WHERE embedding IS NOT NULL")
        emb_md = c.fetchone()[0]
        conn.close()
        return {
            "status": "healthy",
            "api_key_set": bool(API_KEY),
            "discourse_chunks": disc_count,
            "markdown_chunks": md_count,
            "discourse_embeddings": emb_disc,
            "markdown_embeddings": emb_md,
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=500, content={"status": "unhealthy", "error": str(e)}
        )


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
