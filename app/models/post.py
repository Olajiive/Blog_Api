from ..utils import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    author= db.Column(db.String(), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    post_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<post '{self.title}'>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)