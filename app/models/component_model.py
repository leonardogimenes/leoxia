from sqlalchemy.orm import relationship

from app import db


class Component(db.Model):
    __tablename__ = 'component'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.String(140),
        index=False,
        unique=False,
        nullable=True
    )

    on = db.Column(
        db.Boolean,
        index=False,
        unique=False,
        nullable=False
    )

    pins = relationship('Pin', back_populates='component', cascade="all, delete-orphan")

    def __repr__(self):
        return '<Component {}>'.format(self.name)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description, "on": self.on,
                "pins": [pin.to_dict() for pin in self.pins]}
