import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
BOT_NAME = os.getenv("BOT_NAME", "Telegram Smart Bot")

# DuckDuckGo HTML endpoint
DUCKDUCKGO_SEARCH_URL = "https://html.duckduckgo.com/html/"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/100.0 Safari/537.36"
)

# Trusted domain heuristics (prioritize these)
TRUSTED_DOMAINS_PRIORITY = ["github.com", ".org", ".edu", "mozilla.org", "gnu.org"]

# Rate limits
RATE_LIMIT_REQUESTS = 6
RATE_LIMIT_SECONDS = 60

# Maximum results to consider
MAX_RESULTS = 6
