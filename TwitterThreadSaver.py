import tweepy
import webbrowser
import time
import config
import sys

CONSUMER_KEY = config.CONSUMER_KEY
CONSUMER_SECRET = config.CONSUMER_SECRET
callback_uri = config.callback_uri
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
ACCESS_TOKEN = config.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = config.ACCESS_TOKEN_SECRET
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)


def retrieve_last_id(file):
    try:
        f_read = open(file, "r")
        last_seen_id = int(f_read.read().strip())
        f_read.close()
        return last_seen_id
    except Exception as e:
        print("Error occurred!")
        print(e)
        last_seen_id = 0
        return last_seen_id


def store_last_id(last_seen_id, file):
    f_write = open(file, "w")
    f_write.write(str(last_seen_id))
    f_write.close()
    return


FILE = "last_id.txt"


def threadtotext(save_id):
    text_list = []
    while ((api.get_status(save_id)).in_reply_to_status_id != None):
        status_obj = api.get_status(save_id)
        save_id_inreplyto = status_obj.in_reply_to_status_id
        save_id_text = api.get_status(save_id_inreplyto).text
        text_list.append(save_id_text)
        save_id = api.get_status(save_id).in_reply_to_status_id
    text_list.reverse()
    space = ". "
    text = space.join(text_list)
    text_split = text.split(". ")
    for s in text_split[:-1]:
        print(s)
    print(text_split[-1])
    return text


last_seen_id = retrieve_last_id(FILE)
if last_seen_id == 0:
    sys.exit()
else:
    mentions = api.mentions_timeline(last_seen_id, tweet_mode="extended")

for mention in reversed(mentions):
    last_seen_id = mention.id
    store_last_id(last_seen_id, FILE)
    thread_text = threadtotext(last_seen_id)
    direct_message = api.send_direct_message(mention.user.id, thread_text)
