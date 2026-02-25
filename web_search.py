import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

from config import DUCKDUCKGO_SEARCH_URL, USER_AGENT
from .link_validator import filter_links

logger = logging.getLogger(__name__)


def search(query: str, max_results: int = 6) -> List[Dict]:
    headers = {"User-Agent": USER_AGENT}
    params = {"q": query}
    try:
        resp = requests.post(DUCKDUCKGO_SEARCH_URL, data=params, headers=headers, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        logger.exception("Search request failed")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    results = []
    # DuckDuckGo HTML uses 'result' class for results
    for div in soup.select(".result"):
        a = div.find("a", href=True)
        if not a:
            continue
        link = a["href"]
        title = a.get_text(strip=True)
        snippet_tag = div.select_one(".result__snippet") or div.find("a")
        snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""

        results.append({"title": title, "link": link, "snippet": snippet})
        if len(results) >= max_results:
            break

    # Filter and prioritize safe links
    safe = filter_links(results)
    return safe
