import praw
from requests import get
from multiprocessing.pool import ThreadPool
import os
import re



def rid(process_count, image_directory, image_count, target_sub, order):
    def reddit_conn():
        client_id = 'XXXX'
        client_secret = 'XXXX'
        rid_42 = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent='Multithreaded Reddit image downloader thing (by /u/impshum)'
        )
        return rid_42

    def create_tree():
        if not os.path.isdir('./images'):
            os.mkdir('./images')

    def make_dir():
        directory = f'{image_directory}/{target_sub}'
        if not os.path.exists(directory):
            os.makedirs(directory)

    def get_order(reddit, order):
        if order == 'hot':
            ready = reddit.subreddit(target_sub).hot(limit=None)
        elif order == 'top':
            ready = reddit.subreddit(target_sub).top(limit=None)
        elif order == 'new':
            ready = reddit.subreddit(target_sub).new(limit=None)
        return ready

    def get_img(what):
        img = get(what)
        if img.status_code == 200:
            img = img.content
            image = '{}/{}/{}'.format(
                image_directory,
                target_sub,
                what.split('/')[-1]
            )
            with open(image, 'wb') as f:
                f.write(img)

    def check_reddit():
        try:
            reddit.read_only
            return True
        except Exception as e:
            return False

    try:
        if not check_reddit():
            reddit = reddit_conn()
        create_tree()
        make_dir()
        images = []
        order = order.lower()
        c_images = 1
        names = {}

        for submission in get_order(reddit, order):
            url = submission.url
            title = submission.title
            image_name = url.split('/')[-1]
            names.update({image_name: title})
            if url.endswith(('.jpg', '.png', '.gif', '.jpeg')):
                images.append(url)
                c_images += 1
                if int(image_count) < c_images:
                    break
        results = ThreadPool(process_count).imap_unordered(get_img, images)
        for path in results:
            pass
        print(f'RID | {image_count} images | {process_count} processes')

        for filename, name in names.items():
            try:
                name = re.sub("[\(\[].*?[\)\]]", "", name).strip()
                name = re.sub(r'[^\w\s]','',name).replace(' ', '_').lower()
                ext = filename.split('.')[-1]
                old_filename = 'images/{}/{}'.format(target_sub, filename)
                new_filename = 'images/{}/{}.{}'.format(target_sub, name, ext)
                os.rename(old_filename, new_filename)
            except Exception as e:
                pass

    except Exception as e:
        print(f'That RID no worky | {e}')


rid(10, 'images', 10, 'art', 'new')
