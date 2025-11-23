import tweepy
from pytrends.request import TrendReq
import schedule
import time
from config import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET

# Twitter API bağlantısı
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Google Trends bağlantısı
pytrends = TrendReq(hl='tr-TR', tz=180)  # Türkiye saat dilimi

def get_trends():
    # Türkiye için günlük trend kelimeleri
    trending_searches_df = pytrends.trending_searches(pn='turkey')
    trends_list = trending_searches_df[0].tolist()[:5]  # ilk 5 trend
    # Örnek sebep placeholder (istersen daha sonra sebep eklenebilir)
    trends = [{"name": t, "reason": "Popüler arama"} for t in trends_list]
    return trends

def tweet_trend():
    trends = get_trends()
    for trend in trends:
        try:
            tweet_text = f"📈 Bugün Türkiye’de en çok aranan kelime:\n\n“{trend['name']}”\n\nSebep: {trend['reason']}\n\nSence neden? 🤔"
            poll_options = ["Gündem olayı", "Ünlü / Dizi", "Spor", "Ekonomi"]
            poll_duration_minutes = 60  # 1 saat

            api.update_status(
                status=tweet_text,
                poll_options=poll_options,
                poll_duration_minutes=poll_duration_minutes
            )
            print(f"Tweet atıldı: {trend['name']}")
        except Exception as e:
            print(f"Hata: {e}")

# Zamanlama: günde 3 kez
schedule.every().day.at("09:00").do(tweet_trend)
schedule.every().day.at("13:00").do(tweet_trend)
schedule.every().day.at("18:00").do(tweet_trend)

print("Bot başladı, zamanlamalar aktif...")

while True:
    schedule.run_pending()
    time.sleep(60)
