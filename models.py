from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

dev = False

if dev:
    database_name = "gnss"
    database_path = f"postgres://postgres@localhost:5432/{database_name}"
else:
    database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

# -----------------------------------------------------------------------------------------------------------


def setup_db(app, database_path=database_path):
    ''' Binds a flask application and a SQLAlchemy service. '''

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

    if dev:
        migrate = Migrate(app, db)
        # Commented out as will be using flask migrate to sync the db models
        # The commnad "flask db migrate" in cmd replaces this db.create_all()
        # db.create_all()
    else:
        db.create_all()

    return db

# -----------------------------------------------------------------------------------------------------------


class Gnss(db.Model):
    ''' A model for holding a GNSS entry. '''

    __tablename__ = 'gnss'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(16), nullable=False, unique=True)
    owner = Column(db.String(16), nullable=False)
    num_satellites = Column(db.Integer, nullable=False)
    num_frequencies = Column(db.Integer, nullable=False)

    signals = db.relationship('Signal', backref='gnss', lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def cancel(self):
        db.session.rollback()

    def close(self):
        db.session.close()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'owner': self.owner,
            'num_satellites': self.num_satellites,
            'num_frequencies': self.num_frequencies
        }

# -----------------------------------------------------------------------------------------------------------


class Signal(db.Model):
    '''A model for holding a GNSS signal entry.'''

    id = Column(db.Integer, primary_key=True)
    signal = Column(db.String(16), nullable=False)
    gnss_id = Column(db.Integer, db.ForeignKey('gnss.id'))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def cancel(self):
        db.session.rollback()

    def close(self):
        db.session.close()

    def format(self):
        return {
            'id': self.id,
            'signal': self.signal,
            'gnss_id': self.gnss_id,
        }

# -----------------------------------------------------------------------------------------------------------
