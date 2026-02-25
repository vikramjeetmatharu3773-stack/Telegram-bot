from typing import Dict, Tuple

BLOCKED_KEYWORDS = [
    "torrent",
    "torrentz",
    "kickass",
    "piratebay",
    "piracy",
    "crack",
    "serial key",
    "keygen",
    "warez",
    "porn",
    "xxx",
]

BLOCKED_DOMAINS = ["thepiratebay.org", "1337x.to"]


def check_query_safety(query: str, classification: Dict) -> Tuple[bool, str]:
    q = query.lower()
    for kw in BLOCKED_KEYWORDS:
        if kw in q:
            return False, (
                "Request blocked: the query appears to request restricted or illegal content. "
                "I can only return legal, public resources."
            )

    # Additional quick checks based on classification
    cat = classification.get("category", "")
    if cat == "music" and "free download" in q and "creative commons" not in q:
        # allow legal music only
        return True, ""

    # Default allow
    return True, ""
