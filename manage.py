from flask_script import Manager

from backend.src.gnssapi import create_app

app = create_app(test_config=None)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
