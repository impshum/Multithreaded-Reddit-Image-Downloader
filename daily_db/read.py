import pickledb

db = pickledb.load('data/data.db', False)


def main():
    for title in db.getall():
        y = db.get(title).split('|')
        image = y[0]
        author = y[1]
        print(f'title: {title}')
        print(f'image: {image}')
        print(f'author: {author}')


if __name__ == '__main__':
    main()
