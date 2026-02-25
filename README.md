# Telegram Smart Bot

Lightweight, modular Telegram search bot designed to run on Termux (Android). It performs rule-based intent classification, searches the web via DuckDuckGo HTML, scrapes metadata with BeautifulSoup, and returns safe, official public links only.

Features
- Built-in rule-based "AI" for intent classification and query enhancement
- DuckDuckGo HTML search (no API keys)
- Safety filtering (blocks torrents, piracy, adult terms)
- Prioritizes official domains, GitHub, .edu, .org
- Async architecture using python-telegram-bot

Termux setup

1. Update and install Python & git

```bash
pkg update -y
pkg install -y python git
python -m pip install --upgrade pip
```

2. Clone or copy the project into Termux home directory, then install requirements

```bash
cd ~/
git clone <your-repo> telegram-smart-bot
cd telegram-smart-bot
pip install -r requirements.txt
```

3. Create `.env` from `.env.example` and add your Telegram bot token

```bash
cp .env.example .env
# edit .env and set TELEGRAM_BOT_TOKEN
```

4. Run

```bash
python bot.py
```

Usage
- `/start` — welcome message
- `/help` — usage
- `/search <query>` — run a search
- Send a plain text query — the bot will treat it as a search

Notes and limitations
- The bot performs only public web searches and filters results heuristically; it cannot access private or paid data.
- The search uses DuckDuckGo HTML endpoint which may change; parsers are defensive but not infallible.
- For production deployment consider persistence for rate-limiting, caching, and stronger domain allowlists.

License
- MIT-style: reuse and adapt as you wish.
