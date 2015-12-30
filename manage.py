from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os
from minitweet_app import app, db

app.config.from_object(os.environ["CONFIG"])
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
