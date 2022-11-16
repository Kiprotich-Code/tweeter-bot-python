from tweepy import Stream
import logging
from config import create_api
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class FavRetweetListener(Stream):
    def _init_(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:

        #Ignore replies or tweets I author
            return
        if not tweet.favorited:
            try:
                tweet.favorite()
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            logger.error("Error on fav and retweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)

def main(keywords):
    api = create_api()
    stream = FavRetweetListener(api, api.auth)
    # tweets_listener = FavRetweetListener(api)
    # stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"])

if __name__ == "__main__":
    main(["Programming", "MMTVC"])

# class MyStreamListener(Stream):
#     def on_status(self, status):
#         print(status.text)

#     def on_error(self, status_code):
#         if status_code == 420:
#             return False

#     stream = MyStreamListener(
#     consumer_key,
#     consumer_secret,
#     access_token,
#     access_token_secret=
# )

# stream.filter(track=["Programming"], languages=["en"])