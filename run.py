import praw
import threading
from requests import get
from multiprocessing.pool import ThreadPool


client_id = 'XXXX'
client_secret = 'XXXX'
user_agent = 'Multithreaded Reddit image downloader thing (by /u/impshum)'

target_subreddit = input('which subreddit?: ')
image_count = input('how many images?: ')
order = input('hot/new/top?: ')

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)


def get_img(what):
    image = 'zzz/{}'.format(what.split('/')[-1])
    img = get(url).content
    with open(image, 'wb') as f:
        f.write(img)


order = order.lower()

if order == 'hot':
    ready = reddit.subreddit('pics').hot(limit=None)
elif order == 'top':
    ready = reddit.subreddit('pics').top(limit=None)
elif order == 'new':
    ready = reddit.subreddit('pics').new(limit=None)

c = 1
images = []

for submission in ready:
    url = submission.url
    if url.endswith(('.jpg', '.png', '.gif', '.jpeg')):
        images.append(url)
        c += 1
        if int(image_count) < c:
            break

results = ThreadPool(8).imap_unordered(get_img, images)
for path in results:
    print('DONE')
