from datetime import datetime

from hello_flask import db
from models import Post


posts = [
    {
        'author': 'Zain Shah',
        'title': 'Blog Post 1',
        'content': 'First',
        'date_posted': '31 Dec 2018'
    },
    {
        'author': 'John Doe',
        'title': 'Blog Post 2',
        'content': 'Second',
        'date_posted': '01 Jan 2019'
    }
]


def add_posts():
    for post in posts:
        post_obj = Post(author=post['author'], title=post['title'],
                        content=post['content'], date_posted=datetime.strptime(post['date_posted'], '%d %b %Y'))
        db.session.add(post_obj)

    db.session.commit()


def setUp():
    db.create_all()
    add_posts()


if __name__ == '__main__':
    setUp()
