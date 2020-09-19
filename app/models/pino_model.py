from sqlalchemy.orm import relationship

from app import db


class Pino(db.Model):

    __tablename__ = 'pino'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    pino = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )

    component_id = db.Column(
        db.Integer,
        db.ForeignKey('component.id')
    )

    component = relationship('Component', back_populates='pinos')

    def __repr__(self):
        return '<Pino {}>'.format(self.pino)

    def to_dict(self):
        return {"id": self.id, "pino": self.pino}

