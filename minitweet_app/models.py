# ``# pragma: no cover`` is to exclude lines from coverage test
from . import db, bcrypt  # pragma: no cover


class Post(db.Model):

    __tablename__ = "posts"  # pragma: no cover

    id = db.Column(db.Integer, primary_key=True)  # pragma: no cover
    title = db.Column(db.String, nullable=False)  # pragma: no cover
    body = db.Column(db.String, nullable=False)   # pragma: no cover
    # ForeignKey
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # pragma: no cover

    def __init__(self, title,  body, author_id):
        self.title = title
        self.body = body
        self.author_id = author_id

    def __repr__(self):
        # for debugging
        return "<Post {}>".format(self.title)


class User(db.Model):

    __tablename__ = "users"  # pragma: no cover

    id = db.Column(db.Integer, primary_key=True)  # pragma: no cover
    name = db.Column(db.String, nullable=False)  # pragma: no cover
    email = db.Column(db.String, nullable=False)  # pragma: no cover
    password = db.Column(db.String, nullable=False)  # pragma: no cover
    bio = db.Column(db.String)  # pragma: no cover
    website = db.Column(db.String)  # pragma: no cover
    # one to many relationship
    posts = db.relationship("Post", backref="author", lazy="dynamic")  # pragma: no cover
    confirmed = db.Column(db.Boolean, nullable=False, default=False)  # pragma: no cover

    def __init__(self, name, email, password, bio='', website="", confirmed=False):
        self.name = name
        self.email = email
        # generate one way hash for password
        self.password = bcrypt.generate_password_hash(password)
        self.bio = bio
        self.website = website
        self.confirmed = confirmed


    #=========================================#
    #  Flask-Login extension required methods #
    #=========================================#

    def is_authenticated(self):
        return True


    def is_active(self):
        return True


    def is_anonymous(self):
        return False


    def get_id(self):
        return str(self.id)

    def __repr__(self):
        # for debugging
        return '<User {}>'.format(self.name)
