import httpx, json, os

BASE = "https://discourse.onlinedegree.iitm.ac.in"
KEY = os.environ["DISCOURSE_API_KEY"]
USER = os.environ.get("DISCOURSE_API_USER","system")

def fetch_topic(topic_id):
    all_posts = []
    page = 1
    while True:
        r = httpx.get(
            f"{BASE}/t/{topic_id}.json",
            params={"api_key":KEY,"api_username":USER,"page":page}
        )
        data = r.json()
        posts = data["post_stream"]["posts"]
        all_posts += posts
        if len(posts) < 30: break
        page += 1
    return all_posts

if __name__=="__main__":
    # replace <TOPIC_ID> with your actual course-topic ID
    posts = fetch_topic(<YOUR_COURSE_TOPIC_ID>)
    with open("scraped_posts.json","w") as f:
        json.dump(posts, f, indent=2)
