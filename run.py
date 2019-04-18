import praw
import threading
from requests import get
from multiprocessing.pool import ThreadPool
import os


client_id = 'XXXX'
client_secret = 'XXXX'
user_agent = 'Multithreaded Reddit image downloader thing (by /u/impshum)'
image_directory = 'images'
thread_count = 16

target_subreddit = input('Which subreddit?: ')
image_count = input('How many images?: ')
order = input('Hot/New/Top?: ')

order = order.lower()

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret, user_agent=user_agent)


def get_order():
    if order == 'hot':
        ready = reddit.subreddit(target_subreddit).hot(limit=None)
    elif order == 'top':
        ready = reddit.subreddit(target_subreddit).top(limit=None)
    elif order == 'new':
        ready = reddit.subreddit(target_subreddit).new(limit=None)
    return ready


def get_img(what):
    image = '{}/{}/{}'.format(image_directory,
                              target_subreddit, what.split('/')[-1])
    img = get(what).content
    with open(image, 'wb') as f:
        f.write(img)


def make_dir():
    directory = f'{image_directory}/{target_subreddit}'
    if not os.path.exists(directory):
        os.makedirs(directory)


def main():
    c = 1
    images = []
    make_dir()
    for submission in get_order():
        url = submission.url
        if url.endswith(('.jpg', '.png', '.gif', '.jpeg')):
            images.append(url)
            c += 1
            if int(image_count) < c:
                break

    results = ThreadPool(thread_count).imap_unordered(get_img, images)
    for path in results:
        pass

    print('Done')

if __name__ == '__main__':
    main()
