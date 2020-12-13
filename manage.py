from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from backend.src.gnssapi import create_app
from backend.src.database.models import db


app = create_app(test_config=None)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
