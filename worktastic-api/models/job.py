from extensions import db

class Job(db.Model):

    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    salary = db.Column(db.Integer)
    is_published = db.Column(db.Boolean(), default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    @property
    def data(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'salary': self.salary
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_published(cls):
        return cls.query.filter_by(is_published=True).all()

    @classmethod
    def get_by_id(cls, job_id):
        return cls.query.filter_by(id=job_id).first()


