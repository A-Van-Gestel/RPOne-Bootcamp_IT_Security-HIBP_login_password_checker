from sqlalchemy import func

from extensions import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<User: id: {self.id}, email: {self.email}>'

    @staticmethod
    def add_user(email, password):
        user = User(email=email,
                    password=password)

        db.session.add(user)
        db.session.commit()

    @staticmethod
    def remove_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
