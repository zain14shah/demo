from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zainshah:123123@localhost/hello_flask'
db = SQLAlchemy(app)


@app.route('/')
def display_posts():
    from models import Post
    posts = Post.query.all()
    return render_template('show_posts.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
