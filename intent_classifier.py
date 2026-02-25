import re
from typing import Dict

# Simple rule-based intent classifier

CATEGORY_KEYWORDS = {
    "software": ["download", "installer", "setup", "exe", "apk", "software"],
    "pdf": ["pdf", "filetype:pdf", "manual", "paper", "ebook"],
    "image": ["image", "png", "jpg", "photo", "wallpaper"],
    "tutorial": ["tutorial", "how to", "guide", "walkthrough"],
    "dataset": ["dataset", "csv", "kaggle", "data set", "open data"],
    "music": ["mp3", "music", "free music", "creative commons"],
    "open-source": ["open source", "github", "gitlab", "source code"],
}

DOWNLOAD_INTENT_WORDS = ["download", "get", "install", "installer", "free download"]
INFO_INTENT_WORDS = ["what is", "how to", "who is", "guide", "tutorial", "explain"]


def classify_intent(query: str) -> Dict:
    q = query.lower()
    intent = "informational"
    category = "general"
    confidence = 0.5

    # Detect download intent
    if any(w in q for w in DOWNLOAD_INTENT_WORDS):
        intent = "download"
        confidence = 0.8

    # Detect informational
    if any(w in q for w in INFO_INTENT_WORDS):
        intent = "informational"
        confidence = max(confidence, 0.7)

    # Category detection
    for cat, kws in CATEGORY_KEYWORDS.items():
        for kw in kws:
            if kw in q:
                category = cat
                confidence = max(confidence, 0.75)
                break

    # Safe fallback
    return {"intent": intent, "category": category, "confidence": confidence}
