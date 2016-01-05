from . import db, bcrypt


class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    # ForeignKey
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title,  body, author_id):
        self.title = title
        self.body = body
        self.author_id = author_id

    def __repr__(self):
        # for debugging
        return "<Post {}>".format(self.title)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    bio = db.Column(db.String)
    # one to many relationship
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __init__(self, name, email, password, bio=''):
        self.name = name
        self.email = email
        # generate one way hash for password
        self.password = bcrypt.generate_password_hash(password)
        self.bio = bio

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
