# =====================================================
# GLOBAL MARKET + NEWS ANALYSIS TELEGRAM BOT (COLAB)
# Runs ONCE daily at 6:00 PM IST
# =====================================================

import feedparser
import requests
from datetime import datetime
import pytz
from textblob import TextBlob

# -------------------------------
# TELEGRAM CONFIG (FINAL)
# -------------------------------
BOT_TOKEN = "8505207910:AAEoQz_86_4bu412JQK0rJ4gKihgNbuz2vU"
CHAT_ID = "1301385888"

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# -------------------------------
# RSS FEEDS (GLOBAL + INDIA)
# -------------------------------
RSS_FEEDS = [
    # Global
    "https://www.investing.com/rss/news.rss",
    "https://www.investing.com/rss/stock_market_news.rss",
    "https://www.investing.com/rss/commodities.rss",
    "https://www.investing.com/rss/forex.rss",
    "https://www.investing.com/rss/crypto.rss",
    "https://www.reuters.com/rssFeed/businessNews",
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://www.ft.com/?format=rss",
    "https://www.bloomberg.com/markets/rss",

    # India
    "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146843.cms",
    "https://www.moneycontrol.com/rss/latestnews.xml",
    "https://www.nseindia.com/rss/market-news",
    "https://www.bseindia.com/xml-data/corpfilingrss.aspx",

    # Commodities / Forex / Crypto
    "https://www.barchart.com/news/rss/commodities",
    "https://www.barchart.com/news/rss/financials/fx",
    "https://www.barchart.com/news/rss/financials/crypto",
]

# -------------------------------
# MARKET KEYWORDS
# -------------------------------
MARKET_KEYWORDS = {
    "Equity": ["stock", "sensex", "nifty", "dow", "nasdaq", "shares", "ipo"],
    "Forex": ["forex", "usd", "inr", "eur", "currency", "dollar"],
    "Commodities": ["gold", "oil", "crude", "silver", "commodity", "opec"],
    "Crypto": ["bitcoin", "ethereum", "crypto", "btc", "eth"]
}

# -------------------------------
# SENTIMENT → MARKET VIEW
# -------------------------------
def market_view(score):
    if score > 0.15:
        return "📈 BULLISH EXPECTED"
    elif score < -0.15:
        return "📉 BEARISH EXPECTED"
    else:
        return "⚖️ SIDEWAYS / NEUTRAL"

# -------------------------------
# SEND TELEGRAM MESSAGE
# -------------------------------
def send_telegram(message):
    requests.post(
        TELEGRAM_URL,
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
    )

# -------------------------------
# MAIN ANALYSIS LOGIC
# -------------------------------
def run_analysis():
    seen_titles = set()
    collected_news = []

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:3]:
            title = entry.title.strip()

            if title in seen_titles:
                continue
            seen_titles.add(title)

            sentiment = TextBlob(title).sentiment.polarity
            market = "General"

            for mkt, words in MARKET_KEYWORDS.items():
                if any(word in title.lower() for word in words):
                    market = mkt
                    break

            collected_news.append((market, title, sentiment))

    # -------------------------------
    # FORMAT TELEGRAM MESSAGE
    # -------------------------------
    message = "📊 <b>GLOBAL MARKET & NEWS ANALYSIS</b>\n"
    message += "🕕 <b>Time:</b> 6:00 PM IST\n\n"

    for market, title, score in collected_news[:12]:
        message += (
            f"🌍 <b>{market}</b>\n"
            f"<b>Prediction:</b> {market_view(score)}\n"
            f"<b>News:</b> {title}\n\n"
        )

    message += "📌 <i>Auto analysis from global & Indian RSS feeds</i>"

    send_telegram(message)

# -------------------------------
# RUN ONLY AT 6 PM IST
# -------------------------------
def run_if_6pm():
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)

    if now.hour == 18 and now.minute == 0:
        run_analysis()
        print("✅ Telegram market report sent")
    else:
        print("⏳ Not 6 PM IST | Current IST:", now.strftime("%H:%M"))

# -------------------------------
# EXECUTE
# -------------------------------
run_if_6pm()
