from urllib.parse import urlparse


def extract_domain(url: str) -> str:
    try:
        p = urlparse(url)
        return p.netloc
    except Exception:
        return ""
