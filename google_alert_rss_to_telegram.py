import feedparser
import requests
import time

# Configuration
RSS_URL_LIST = [
"https://www.google.co.in/alerts/feeds/06660699284050266053/9479878068789660271",
"https://www.google.co.in/alerts/feeds/06660699284050266053/3248098847498370551",
"https://www.google.co.in/alerts/feeds/06660699284050266053/1774105227142705003",
"https://www.google.co.in/alerts/feeds/06660699284050266053/16270256872332916796",
"https://www.google.com/alerts/feeds/06660699284050266053/12485566338060611844", #UGEE
"https://www.google.com/alerts/feeds/06660699284050266053/12485566338060613940", #JAC Delhi
"https://www.google.com/alerts/feeds/06660699284050266053/9346545140038872930", #MBBS
"https://www.google.com/alerts/feeds/06660699284050266053/10620334520593906679", #VITEEE
"https://www.google.com/alerts/feeds/06660699284050266053/14453981990149627571", #SITEEE
"https://www.google.com/alerts/feeds/06660699284050266053/13147617054575588815" #MET Manipal
]

BOT_TOKEN = "8526202388:AAG5bD6MSaHBh1Fzk042J5cYYmcC-PwgD84"
CHAT_ID = "@vs_whatsapp_api_alerts"  # Group IDs usually start with a minus sign (-)

# Track seen entries to avoid duplicates
seen_entries = set()


def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    requests.post(url, data=payload)


def check_alerts():
    print("Checking for new alerts...")
    feed = feedparser.parse(RSS_URL)

    for entry in feed.entries:
        if entry.id not in seen_entries:
            # Format the message
            message = f"<b>{entry.title}</b>\n<a href='{entry.link}'>Read more</a>"
            send_telegram_msg(message)
            seen_entries.add(entry.id)


if __name__ == "__main__":
    # First run: populate 'seen' so you don't get 20 old alerts immediately
    while True:
        for RSS_URL in RSS_URL_LIST:
            initial_feed = feedparser.parse(RSS_URL)
            for entry in initial_feed.entries:
                seen_entries.add(entry.id)
                check_alerts()
        time.sleep(600)  # Check every 10 minutes