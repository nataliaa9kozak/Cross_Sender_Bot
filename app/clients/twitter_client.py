from .client import SocialClient
import tweepy
from app.base.settings import (
    TWITTER_BEARER_TOKEN,
    TWITTER_API_KEY,
    TWITTER_API_SECRET_KEY,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
)
import time


class TwitterClient(SocialClient):
    def __init__(self) -> None:
        self.client_v2 = tweepy.Client(
            bearer_token=TWITTER_BEARER_TOKEN,
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET_KEY,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
        )
        self.auth = tweepy.OAuth1UserHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        self.client_v1 = tweepy.API(self.auth)

    def send_message(self, message, media_ids=None):
        retries = 3
        for _ in range(retries):
            try:
                response = self.client_v2.create_tweet(
                    text=message,
                    media_ids=media_ids
                )
                print("Tweet sent:", response)
                return True
            except tweepy.TweepyException as e:
                print(f"Error: {e}")
                time.sleep(5)
        print("Failed to send tweet after retries")
        return False

    def send_media(self, file, file_name=None):
        self.client_v1.media_upload(filename='image.jpg', file=file)
