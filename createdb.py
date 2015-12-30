from minitweet_app import db, models

# create all tables
db.create_all()

# test data

db.session.add(models.Post("test", "test", "test"))
db.session.commit()
