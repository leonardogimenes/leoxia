from app import db


class User(db.Model):

    __tablename__ = 'user'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )

    group = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "group": self.group}

