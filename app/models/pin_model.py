from sqlalchemy.orm import relationship

from app import db


class Pin(db.Model):

    __tablename__ = 'pin'
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

    component_id = db.Column(
        db.Integer,
        db.ForeignKey('component.id'),
        nullable=False
    )

    component = relationship('Component', back_populates='pins')

    def __repr__(self):
        return '<Pin {}>'.format(self.name)

    def to_dict(self):
        return {"id": self.id, "pin": self.name}

