import praw
import schedule
from requests import get
from time import sleep
from multiprocessing.pool import ThreadPool
import os
from datetime import datetime
import pickledb


client_id = 'XXXX'
client_secret = 'XXXX'
target_subreddit = 'EarthPorn'
image_directory = 'data'
image_count = 2
order = 'top'
schedule_time = '09:00'
thread_count = 4

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret, user_agent='Reddit downloader thing (by /u/impshum)')

if not os.path.exists('data'):
    os.makedirs('data')
    
db = pickledb.load('data/data.db', False)


def get_order():
    if order == 'hot':
        ready = reddit.subreddit(target_subreddit).hot(limit=None)
    elif order == 'top':
        ready = reddit.subreddit(target_subreddit).top(limit=None)
    elif order == 'new':
        ready = reddit.subreddit(target_subreddit).new(limit=None)
    return ready


def do_db(k, v, u):
    if not db.exists(k):
        db.set(k, f'{v}|{u}')
        db.dump()
        return True
    else:
        return False


def get_img(today, title, url, author):
    image = '{}/{}'.format(today, url.split('/')[-1])
    if do_db(title, image, author):
        img = get(url).content
        with open(image, 'wb') as f:
            f.write(img)


def make_dir():
    dir = datetime.today().strftime('%d-%m-%Y')
    directory = f'{image_directory}/{dir}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    return [dir, directory]


def main():
    c = 1
    mkdir = make_dir()
    done = mkdir[0]
    today = mkdir[1]
    for submission in get_order():
        url = submission.url
        title = submission.title
        author = submission.author.name
        if url.endswith(('.jpg', '.png', '.gif', '.jpeg', '.gif')):
            get_img(today, title,  url, author)
            c += 1
            if image_count < c:
                break

    print(f'Done {done}')


if __name__ == '__main__':
    main()
    schedule.every().day.at(schedule_time).do(main)
    while True:
        schedule.run_pending()
        sleep(1)
