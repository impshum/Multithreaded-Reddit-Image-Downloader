import praw
import schedule
import threading
from requests import get
from time import sleep
from multiprocessing.pool import ThreadPool
import os
from datetime import datetime


client_id = 'XXXX'
client_secret = 'XXXX'
user_agent = 'Multithreaded daily Reddit image downloader thing (by /u/impshum)'
target_subreddit = 'EarthPorn'
image_directory = 'images'
image_count = 10
schedule_time = '09:00'
thread_count = 4

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret, user_agent=user_agent)



def get_img(what):
    dir = datetime.today().strftime('%d-%m-%Y')
    image = '{}/{}/{}'.format(image_directory, dir, what.split('/')[-1])
    img = get(what).content
    with open(image, 'wb') as f:
        f.write(img)


def make_dir():
    dir = datetime.today().strftime('%d-%m-%Y')
    directory = f'{image_directory}/{dir}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    return dir


def main():
    c = 1
    images = []
    today = make_dir()
    for submission in reddit.subreddit(target_subreddit).new(limit=None):
        url = submission.url
        if url.endswith(('.jpg', '.png', '.gif', '.jpeg')):
            images.append(url)
            c += 1
            if int(image_count) < c:
                break

    results = ThreadPool(thread_count).imap_unordered(get_img, images)
    for path in results:
        pass

    print(f'Done {today}')


if __name__ == '__main__':
    main()
    schedule.every().day.at(schedule_time).do(main)
    while True:
        schedule.run_pending()
        sleep(1)
