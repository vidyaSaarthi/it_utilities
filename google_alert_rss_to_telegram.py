import feedparser
import requests
import time

# Configuration
RSS_URL_LIST = [
"https://www.google.co.in/alerts/feeds/06660699284050266053/9479878068789660271", #BITSAT
"https://www.google.co.in/alerts/feeds/06660699284050266053/3248098847498370551", #COMEDK
"https://www.google.co.in/alerts/feeds/06660699284050266053/1774105227142705003", #JEE
"https://www.google.co.in/alerts/feeds/06660699284050266053/16270256872332916796", #NEET
"https://www.google.com/alerts/feeds/06660699284050266053/12485566338060611844", #UGEE
"https://www.google.com/alerts/feeds/06660699284050266053/12485566338060613940", #JAC Delhi
"https://www.google.com/alerts/feeds/06660699284050266053/9346545140038872930", #MBBS
"https://www.google.com/alerts/feeds/06660699284050266053/10620334520593906679", #VITEEE
"https://www.google.com/alerts/feeds/06660699284050266053/14453981990149627571", #SITEEE
"https://www.google.com/alerts/feeds/06660699284050266053/13147617054575588815", #MET Manipal
"https://www.google.com/alerts/feeds/06660699284050266053/10438470197552500086" #CUET
"https://www.google.com/alerts/feeds/06660699284050266053/5387349637885216539", #NISER
"https://www.google.com/alerts/feeds/06660699284050266053/1287242344672731619", #IISER
"https://www.google.com/alerts/feeds/06660699284050266053/3680806040444127722" #DAICT
"https://www.google.com/alerts/feeds/06660699284050266053/5213746017576248862", #JOSAA
"https://www.google.com/alerts/feeds/06660699284050266053/11662474502245257093", #JIIT
"https://www.google.com/alerts/feeds/06660699284050266053/4933146280845086354", #JAYPEE INSTITUTE OF INFORMATION TECHNOLOGY
"https://www.google.com/alerts/feeds/06660699284050266053/15015340571517855658", #HSTES
"https://www.google.com/alerts/feeds/06660699284050266053/15482280052394751531", #JAC Chandigarh
"https://www.google.com/alerts/feeds/06660699284050266053/15482280052394752618", #SRMJEE
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