import re
from typing import List, Dict
from urllib.parse import urlparse

from config import TRUSTED_DOMAINS_PRIORITY

SUSPICIOUS_PATTERNS = [r"torrent", r"\.zip$", r"\.exe$", r"keygen", r"crack"]


def domain_score(domain: str) -> int:
    score = 0
    for d in TRUSTED_DOMAINS_PRIORITY:
        if d in domain:
            score += 10
    return score


def is_suspicious(url: str) -> bool:
    low = url.lower()
    for p in SUSPICIOUS_PATTERNS:
        if re.search(p, low):
            return True
    return False


def validate_url(url: str) -> bool:
    try:
        p = urlparse(url)
        return p.scheme in ("http", "https") and p.netloc
    except Exception:
        return False


def filter_links(results: List[Dict]) -> List[Dict]:
    cleaned = []
    for r in results:
        link = r.get("link")
        if not link or not validate_url(link):
            continue
        if is_suspicious(link):
            continue
        cleaned.append(r)

    # Sort by domain priority
    cleaned.sort(key=lambda x: domain_score(urlparse(x.get("link")).netloc), reverse=True)
    return cleaned
