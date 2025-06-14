import os
import json
from fastapi import FastAPI
from pydantic import BaseModel

BASE_URL = os.environ.get("DISCOURSE_BASE", "https://discourse.onlinedegree.iitm.ac.in")

# Load scraped posts (must exist)
with open("scraped_posts.json") as f:
    posts = json.load(f)

app = FastAPI()


class Query(BaseModel):
    question: str
    image: str = None


@app.post("/api/")
async def answer(q: Query):
    # Simple substring match
    for post in posts:
        if q.question.lower() in post.get("cooked", "").lower():
            return {
                "answer": post["cooked"][:200] + "...",
                "links": [
                    {
                        "url": f"{BASE_URL}/t/{post['topic_id']}/{post['post_number']}",
                        "text": "Source",
                    }
                ],
            }
    return {"answer": "Sorry, I don’t know.", "links": []}
