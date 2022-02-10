from extensions import db
from passlib.hash import pbkdf2_sha256

class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200))
    jobs = db.relationship('Job', backref='user')

    @property
    def data(self):
        return {
            'id': self.id,
            'username': self.username
        }

    @classmethod
    def hash_password(cls, password):
        return pbkdf2_sha256.hash(password)

    @classmethod
    def verify_password(cls, password, hashed):
        return pbkdf2_sha256.verify(password, hashed)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
