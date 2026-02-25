from typing import Dict, List
from utils.helpers import extract_domain


def format_results_message(original_query: str, classification: Dict, results: List[Dict]) -> str:
    lines = []
    lines.append(f"🔎 Results for: {original_query}")
    lines.append(f"Intent: {classification.get('intent')} | Category: {classification.get('category')}")
    lines.append("")

    if not results:
        lines.append("No safe results found. Try refining your query.")
        return "\n".join(lines)

    for i, r in enumerate(results, start=1):
        title = r.get("title") or "(no title)"
        link = r.get("link")
        snippet = r.get("snippet") or ""
        domain = extract_domain(link) if link else ""

        lines.append(f"{i}. {title}")
        if domain:
            lines.append(f"   🏷️ {domain}")
        if snippet:
            lines.append(f"   📝 {snippet}")
        if link:
            lines.append(f"   🔗 {link}")
        lines.append("")

    lines.append("✅ Only official/public sources prioritized. Use responsibly.")
    return "\n".join(lines)
