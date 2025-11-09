from fastapi import FastAPI, Query
import requests
from datetime import datetime

app = FastAPI(title="Scholar Service (Debug)")

@app.get("/scholar")
def get_scholar(author: str = Query(..., description="Author name to look up")):
    try:
        url = (
            f"https://api.semanticscholar.org/graph/v1/author/search"
            f"?query={author}&limit=1&fields=name,affiliations,hIndex,citationCount,url"
        )
        print(f"🔎 Fetching: {url}")  # log the URL being called
        response = requests.get(url, timeout=15)
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text[:500]}")  # log first 500 chars

        if response.status_code != 200:
            return {"status": "error", "message": f"HTTP {response.status_code}"}

        data = response.json()
        if not data.get("data"):
            return {"status": "error", "message": "Author not found"}

        author_data = data["data"][0]
        summary = {
            "name": author_data.get("name"),
            "affiliation": author_data.get("affiliations"),
            "h_index": author_data.get("hIndex"),
            "citations": author_data.get("citationCount"),
            "profile_url": author_data.get("url"),
            "checked_at": datetime.utcnow().isoformat(),
        }
        return {"status": "success", "data": summary}

    except Exception as e:
        print(f"❌ Exception: {e}")
        return {"status": "error", "message": str(e)}
