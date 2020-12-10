# GNSS API Backend

## Getting Started

Note: The instructions below are for a Windows 10 platform.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### Python 3.8 Addendum

Install https://visualstudio.microsoft.com/visual-cpp-build-tools

Go into backend\env\Lib\site-packages\sqlalchemy\util\compat.py and follow the instructions here: https://knowledge.udacity.com/questions/132762#132817
Also: pip install --upgrade Werkzeug

## Database Setup

With Postgres running:

```
pg_ctl -D "C:\Program Files\PostgreSQL\13\data" start
createdb -U postgres gnss
```

Run the following commands to create the postgres db schema (no GNSS data will be populated):

```
flask db init
flask db migrate
flask db upgrade
```