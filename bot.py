import feedparser
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TELEGRAM_BOT_TOKEN = "8820159092:AAHJdFQjHkOwJN-HxS4Na7HR_gPzhCQQu0s"
TELEGRAM_CHAT_ID = "6798894448"

ACCOUNTS = ["AJArabic","khaled_9733","jaber_j","BBCArabic"]
KEYWORDS = [,"البحرين", "الملك حمد", "Bahrain","الشيعة","الشيخ ناصر","بسام المعراج","وزير الداخلية", "المنامة"]
NITTER = ["https://nitter.privacydev.net", "https://nitter.poast.org"]

last_seen = {}

def has_keyword(text):
    return any(k.lower() in text.lower() for k in KEYWORDS)

def get_tweets(account):
    for n in NITTER:
        try:
            f = feedparser.parse(f"{n}/{account}/rss")
            if f.entries:
                return f.entries
        except:
            pass
    return []

async def check(bot):
    for acc in ACCOUNTS:
        entries = get_tweets(acc)
        if not entries:
            continue
        e = entries[0]
        eid = e.get("id", e.get("link", ""))
        if last_seen.get(acc) == eid:
            continue
        last_seen[acc] = eid
        if has_keyword(e.get("title", "") + e.get("summary", "")):
            await bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=f"🔔 @{acc}\n\n{e.get('title','')}\n\n{e.get('link','')}",
            )

async def job(context):
    await check(context.bot)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت شغال!")

async def now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 جاري الفحص...")
    await check(context.bot)
    await update.message.reply_text("✅ انتهى!")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", now))
    app.job_queue.run_repeating(job, interval=300, first=10)
    print("✅ البوت شغال!")
    app.run_polling()

if __name__ == "__main__":
    main()