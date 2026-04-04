import feedparser
import requests
import pickle
import os
import time

# Telegram Bot Token
BOT_TOKEN = "8526202388:AAG5bD6MSaHBh1Fzk042J5cYYmcC-PwgD84"
CHAT_ID = "@vs_whatsapp_api_alerts"  # Group IDs usually start with a minus sign (-)
CHAT_ID_NEWS = "@news_update_sa"
new_data_found = False

RSS_TO_GROUP = {
    "https://www.google.co.in/alerts/feeds/06660699284050266053/9479878068789660271" : "@vs_whatsapp_api_alerts", #BITSAT
    "https://www.google.co.in/alerts/feeds/06660699284050266053/3248098847498370551" : "@vs_whatsapp_api_alerts", #COMEDK
    "https://www.google.co.in/alerts/feeds/06660699284050266053/1774105227142705003" : "@vs_whatsapp_api_alerts", #JEE
    "https://www.google.co.in/alerts/feeds/06660699284050266053/16270256872332916796" : "@vs_whatsapp_api_alerts", #NEET
    "https://www.google.com/alerts/feeds/06660699284050266053/12485566338060611844" : "@vs_whatsapp_api_alerts", #UGEE
    "https://www.google.com/alerts/feeds/06660699284050266053/12485566338060613940" : "@vs_whatsapp_api_alerts", #JAC Delhi
    "https://www.google.com/alerts/feeds/06660699284050266053/9346545140038872930" : "@vs_whatsapp_api_alerts", #MBBS
    "https://www.google.com/alerts/feeds/06660699284050266053/10620334520593906679" : "@vs_whatsapp_api_alerts", #VITEEE
    "https://www.google.com/alerts/feeds/06660699284050266053/14453981990149627571" : "@vs_whatsapp_api_alerts", #SITEEE
    "https://www.google.com/alerts/feeds/06660699284050266053/13147617054575588815" : "@vs_whatsapp_api_alerts", #MET Manipal
    "https://www.google.com/alerts/feeds/06660699284050266053/10438470197552500086" : "@vs_whatsapp_api_alerts", #CUET
    "https://www.google.com/alerts/feeds/06660699284050266053/5387349637885216539" : "@vs_whatsapp_api_alerts", #NISER
    "https://www.google.com/alerts/feeds/06660699284050266053/1287242344672731619" : "@vs_whatsapp_api_alerts", #IISER
    "https://www.google.com/alerts/feeds/06660699284050266053/3680806040444127722" : "@vs_whatsapp_api_alerts", #DAICT
    "https://www.google.com/alerts/feeds/06660699284050266053/5213746017576248862" : "@vs_whatsapp_api_alerts", #JOSAA
    "https://www.google.com/alerts/feeds/06660699284050266053/11662474502245257093" : "@vs_whatsapp_api_alerts", #JIIT
    "https://www.google.com/alerts/feeds/06660699284050266053/4933146280845086354" : "@vs_whatsapp_api_alerts", #JAYPEE INSTITUTE OF INFORMATION TECHNOLOGY
    "https://www.google.com/alerts/feeds/06660699284050266053/15015340571517855658" : "@vs_whatsapp_api_alerts", #HSTES
    "https://www.google.com/alerts/feeds/06660699284050266053/15482280052394751531" : "@vs_whatsapp_api_alerts", #JAC Chandigarh
    "https://www.google.com/alerts/feeds/06660699284050266053/15482280052394752618" : "@vs_whatsapp_api_alerts", #SRMJEE
    "https://timesofindia.indiatimes.com/rssfeedmostrecent.cms" : "@news_update_sa", #TOI News
    "https://openai.com/news/rss.xml" : "@ai_news_sa",
    "https://ai.googleblog.com/feeds/posts/default" : "@ai_news_sa",
    "https://deepmind.com/blog/feed/basic/" : "@ai_news_sa",
    "https://blogs.nvidia.com/blog/category/ai/feed/" : "@ai_news_sa",
    "https://huggingface.co/blog/feed.xml" : "@ai_news_sa",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed/" : "@ai_news_sa",
    "https://www.aitrends.com/feed/" : "@ai_news_sa",
    "https://www.marktechpost.com/feed/" : "@ai_news_sa",
    "https://aiweekly.co/feed" : "@ai_news_sa",
    "https://theaireport.com/feed/" : "@ai_news_sa",
    "https://rss.arxiv.org/rss/cs.AI" : "@ai_news_sa",
    "https://distill.pub/rss.xml" : "@ai_news_sa",
    "https://thegradient.pub/rss/" : "@ai_news_sa",
    "https://bair.berkeley.edu/blog/feed.xml" : "@ai_news_sa",
    "https://www.analyticsvidhya.com/feed/" : "@ai_news_sa",
    "https://www.datasciencecentral.com/main/feed/" : "@ai_news_sa",
    "https://www.predictiveanalyticsworld.com/machinelearningtimes/feed/" : "@ai_news_sa"

}

SEEN_FILE = "seen_entries.pkl"

# -------------------------
# Load seen entries
# -------------------------
def load_seen_entries():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "rb") as f:
            return pickle.load(f)
    return set()


# -------------------------
# Save seen entries
# -------------------------
def save_seen_entries(seen_entries):
    with open(SEEN_FILE, "wb") as f:
        pickle.dump(seen_entries, f)


seen_entries = load_seen_entries()


def send_telegram_msg(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }
    requests.post(url, data=payload)


def check_alerts():
    global seen_entries
    print("Checking for new alerts...")

    new_data_found = False

    for rss_url, chat_id in RSS_TO_GROUP.items():
        feed = feedparser.parse(rss_url)

        for entry in feed.entries:
            unique_id = entry.get("id", entry.get("link"))

            if unique_id not in seen_entries:
                message = f"<b>{entry.title}</b>\n<a href='{entry.link}'>Read more</a>"
                send_telegram_msg(chat_id, message)

                seen_entries.add(unique_id)
                new_data_found = True

    # Save only if new entries found (efficient)
    if new_data_found:
        save_seen_entries(seen_entries)


if __name__ == "__main__":
    while True:
        check_alerts()
        print("Sleeping for 10 mins")
        time.sleep(600)
