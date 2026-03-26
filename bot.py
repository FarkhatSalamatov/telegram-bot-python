import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

# === КОМАНДЫ ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 Crypto Price", callback_data="crypto")],
        [InlineKeyboardButton("🌤 Weather", callback_data="weather")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Welcome! I'm your assistant bot.\n\nChoose an option:",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Main menu\n"
        "/help - Show this message\n"
        "/price <coin> - Get crypto price (e.g. /price bitcoin)\n"
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import urllib.request, json
    if not context.args:
        await update.message.reply_text("Usage: /price <coin>\nExample: /price bitcoin")
        return
    coin = context.args[0].lower()
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read())
        if coin in data:
            usd = data[coin]["usd"]
            await update.message.reply_text(f"💰 {coin.capitalize()}: ${usd:,.2f} USD")
        else:
            await update.message.reply_text(f"Coin '{coin}' not found.")
    except Exception as e:
        await update.message.reply_text("Failed to fetch price. Try again later.")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "crypto":
        await query.edit_message_text("Send: /price bitcoin\nor /price ethereum")
    elif query.data == "weather":
        await query.edit_message_text("🌤 Weather feature coming soon!")
    elif query.data == "about":
        await query.edit_message_text("🤖 This bot was built with Python & python-telegram-bot library.\nFeatures: inline keyboards, API integration, command handling.")

# === MAIN ===

if __name__ == "__main__":
    TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your token from @BotFather
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot is running...")
    app.run_polling()
