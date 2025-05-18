import logging
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === SET YOUR API KEYS ===
BOT_TOKEN = "7938014256:AAEhgVZPgNdPvXOh4eLTQ5O6UmQA0W6-zRs"
NEWS_API_KEY = "85833f2a3c5d438ab471054f52601eb1"  # replace with your own if needed

logging.basicConfig(level=logging.INFO)

def get_news(category):
    if category == "forex":
        query = "forex OR EURUSD OR GBPUSD OR US30"
    elif category == "crypto":
        query = "bitcoin OR ethereum OR crypto OR BTC OR ETH"
    elif category == "gold":
        query = "gold OR XAUUSD"
    elif category == "oil":
        query = "oil OR WTI OR Brent"
    elif category == "indices":
        query = "indices OR S&P500 OR NASDAQ OR US30 OR Dow Jones"
    elif category == "economy":
        query = "economic news OR inflation OR interest rates OR central bank"
    else:
        return "Invalid category."

    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])

    if not articles:
        return "No news found."

    news = f"🗞️ Latest {category.capitalize()} News:\n\n"
    for article in articles:
        news += f"• {article['title']}\n{article['url']}\n\n"
    return news

# === HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Forex News Bot!\n\nCommands:\n"
        "/news_forex - Latest Forex News\n"
        "/news_crypto - Latest Crypto News\n"
        "/news_gold - Latest Gold News\n"
        "/news_oil - Latest Oil News\n"
        "/news_indices - Market Indices\n"
        "/news_economy - Economic News"
    )

async def news_forex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fetching Forex news...")
    news = get_news("forex")
    await update.message.reply_text(news)

async def news_crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fetching Crypto news...")
    news = get_news("crypto")
    await update.message.reply_text(news)

async def news_gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fetching Gold news...")
    news = get_news("gold")
    await update.message.reply_text(news)

async def news_oil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fetching Oil news...")
    news = get_news("oil")
    await update.message.reply_text(news)

async def news_indices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fetching Indices news...")
    news = get_news("indices")
    await update.message.reply_text(news)

async def news_economy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fetching Economic news...")
    news = get_news("economy")
    await update.message.reply_text(news)

# === MAIN ===
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("news_forex", news_forex))
    app.add_handler(CommandHandler("news_crypto", news_crypto))
    app.add_handler(CommandHandler("news_gold", news_gold))
    app.add_handler(CommandHandler("news_oil", news_oil))
    app.add_handler(CommandHandler("news_indices", news_indices))
    app.add_handler(CommandHandler("news_economy", news_economy))

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
