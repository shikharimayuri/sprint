from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class user(db.Model):
    id=db.Column(db.Integet , primary_key=True)
    username=db.Column(db.String(80), unique=True, nullable=False)
    password=db.Column(db.Srinng(200),nullable=False)
    