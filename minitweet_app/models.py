from . import db, bcrypt


class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title,  body, author_id):
        self.title = title
        self.body = body
        self.author_id = author_id

    def __repr__(self):
        return "<post {}>".format(self.title)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        # Encrypt password
        self.password = bcrypt.generate_password_hash(password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User {}'.format(self.name)
