import feedparser
import requests
import time

BOT_TOKEN = '7938014256:AAEhgVZPgNdPvXOh4eLTQ5O6UmQA0W6-zRs'
CHAT_ID = '6652848425'

IMPORTANT_KEYWORDS = ['fomc', 'cpi', 'nfp', 'interest rate', 'fed', 'inflation', 'ecb', 'central bank']

RSS_FEEDS = [
    'https://www.forexlive.com/feed/',
    'https://www.dailyfx.com/feeds/news',
    'https://www.investing.com/rss/news_25.rss'
]

ECONOMIC_CALENDAR_RSS = 'https://nfs.faireconomy.media/ff_calendar_thisweek.xml'

def send_to_telegram(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'Markdown'}
    requests.post(url, data=payload)
    time.sleep(1)

def get_filtered_news():
    for rss in RSS_FEEDS:
        feed = feedparser.parse(rss)
        for entry in feed.entries[:5]:
            title = entry.title.lower()
            if any(k in title for k in IMPORTANT_KEYWORDS):
                message = f"*{entry.title}*\n{entry.link}"
                send_to_telegram(message)

def get_upcoming_events():
    feed = feedparser.parse(ECONOMIC_CALENDAR_RSS)
    events = []
    for entry in feed.entries[:10]:
        title = entry.title
        if any(k in title.lower() for k in IMPORTANT_KEYWORDS):
            events.append(f"- {title}")
    if events:
        message = "*Upcoming Economic Events:*\n" + "\n".join(events)
        send_to_telegram(message)

if __name__ == "__main__":
    while True:
        print("Checking forex news and events...")
        get_filtered_news()
        get_upcoming_events()
        print("Sleeping 1 hour...")
        time.sleep(3600)
