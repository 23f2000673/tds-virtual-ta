import os
import httpx
import json

BASE = "https://discourse.onlinedegree.iitm.ac.in"
client = httpx.Client()

# Cookie‐based auth (export these tomorrow)
client.cookies.set(
    "_forum_session",
    os.getenv("DISCOURSE_SESSION_COOKIE", ""),
    domain="discourse.onlinedegree.iitm.ac.in",
)
client.cookies.set(
    "_t",
    os.getenv("DISCOURSE_T_COOKIE", ""),
    domain="discourse.onlinedegree.iitm.ac.in",
)


def fetch_topic(topic_id: int) -> list[dict]:
    posts, page = [], 1
    while True:
        r = client.get(f"{BASE}/t/{topic_id}.json", params={"page": page})
        r.raise_for_status()
        batch = r.json()["post_stream"]["posts"]
        posts.extend(batch)
        if len(batch) < 30:
            break
        page += 1
    return posts


if __name__ == "__main__":
    # TODO: replace 12345 with your TDS topic ID
    all_posts = fetch_topic(12345)
    with open("scraped_posts.json", "w") as f:
        json.dump(all_posts, f, indent=2)
    print(f"Saved {len(all_posts)} posts to scraped_posts.json")
