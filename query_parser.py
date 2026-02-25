from typing import Dict

def enhance_query(query: str, classification: Dict) -> str:
    q = query.strip()
    cat = classification.get("category", "general")
    intent = classification.get("intent", "informational")

    enhancements = []
    # For download intent, prefer official + free keywords
    if intent == "download":
        enhancements.extend(["official site", "free download"])

    # For open-source, emphasize GitHub
    if cat == "open-source":
        enhancements.append("github")

    # For academic/pdf queries
    if cat == "pdf":
        enhancements.extend(["filetype:pdf", "official"])

    # For datasets
    if cat == "dataset":
        enhancements.extend(["dataset", "open data", "kaggle OR data.gov OR " "site:github.com"])

    # Combine while avoiding duplicates
    for e in enhancements:
        if e and e not in q:
            q = f"{q} {e}"

    return q
