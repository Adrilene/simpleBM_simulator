from project import db


class SmartTv(db.Model):
    __tablename__ = "smart_tv"
    id = db.Column(
        db.Integer,
        unique=True,
        nullable=False,
        primary_key=True
    )
    block = db.Column(
        db.Boolean,
        nullable=True
    )
