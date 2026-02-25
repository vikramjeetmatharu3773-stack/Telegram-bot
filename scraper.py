import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def scrape_metadata(url: str) -> dict:
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
    except Exception:
        return {}

    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else None
    desc = None
    m = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
    if m and m.get("content"):
        desc = m.get("content").strip()

    return {"title": title, "description": desc}
