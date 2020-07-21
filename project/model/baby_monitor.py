from project import db
from datetime import datetime

# Babymonitor -> envia dados + status ou dados + notificação
# Babymonitor -> recebe confirmações


class BabyMonitorSend(db.Model):
    """ type: status or notification """

    __tablename__ = "baby_monitor_send"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    crying = db.Column(db.Boolean, nullable=False)
    sleeping = db.Column(db.Boolean, nullable=False)
    breathing = db.Column(db.Boolean, nullable=False)
    time_no_breathing = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(80), nullable=False)
    time = db.Column(db.DateTime, nullable=False)


class BabyMonitorReceive(db.Model):
    """ type: confirmation / ??? """

    __tablename__ = "baby_monitor_receive"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    type = db.Column(db.String(80), nullable=True, default="confirmation")
    time = db.Column(db.DateTime, nullable=False)
    id_notification = db.Column(db.Integer, db.ForeignKey("baby_monitor_send.id"))
