from . import db


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    body = db.Column(db.String)

    def __init__(self, title, author, body):
        self.title = title
        self.author = author
        self.body = body

    def __repr__(self):
        return "<post {}>".format(self.title)
