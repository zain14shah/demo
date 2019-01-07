from datetime import datetime

from hello_flask import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100))
    title = db.Column(db.String(50))
    content = db.Column(db.String(100))
    date_posted = db.Column(db.DateTime(120))

    def __repr__(self):
        return f'Post("{self.author}", "{self.title}", "{self.content}", "{self.date_posted}")'
