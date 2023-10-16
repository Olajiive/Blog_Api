from ..utils import db

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.Text(), nullable=False)
    post = db.relationship("Post", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)