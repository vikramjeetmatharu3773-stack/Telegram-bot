import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from config import TELEGRAM_BOT_TOKEN, BOT_NAME
from intent_classifier import classify_intent
from query_parser import enhance_query
from safety_filter import check_query_safety
from response_formatter import format_results_message
from web_search import search
from rate_limiter import RateLimiter
from logger import setup_logging

load_dotenv()
setup_logging()
logger = logging.getLogger(__name__)

rate_limiter = RateLimiter()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Hello! I'm {BOT_NAME}. Send a query or use /search <query>. I return safe, public resources."
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/search <query> — search the web\nJust send any text and I'll search for it."
    )


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not rate_limiter.allow(user_id):
        await update.message.reply_text("Rate limit exceeded. Please wait a bit and try again.")
        return

    query = " ".join(context.args) if context.args else ""
    if not query:
        await update.message.reply_text("Please provide a search query. Usage: /search <query>")
        return
    await handle_query(update, context, query)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not rate_limiter.allow(user_id):
        await update.message.reply_text("Rate limit exceeded. Please wait a bit and try again.")
        return
    query = update.message.text
    await handle_query(update, context, query)


async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE, query: str):
    msg = await update.message.reply_text("Processing your query... 🔎")
    try:
        classification = classify_intent(query)
        safe, reason = check_query_safety(query, classification)
        if not safe:
            await msg.edit_text(reason)
            return

        enhanced = enhance_query(query, classification)

        # Run web search in thread to avoid blocking
        results = await asyncio.to_thread(search, enhanced, max_results=6)

        # Format top 3
        text = format_results_message(query, classification, results[:3])
        await msg.edit_text(text)
    except Exception:
        logger.exception("Error handling query")
        await msg.edit_text("An error occurred while processing your request.")


def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN not set in environment")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    logger.info("Bot starting")
    app.run_polling()


if __name__ == "__main__":
    main()
