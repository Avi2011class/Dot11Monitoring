try:
    from ..app import db, login
except Exception:
    from app import db, login

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# auth models
class User(UserMixin, db.Model):
    __tablename__ = "users"
    __table_args__ = {"schema": "private"}
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    is_collector = db.Column(db.Boolean, default=False)
    is_viewer = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_sql = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# dot11 models
class Auth(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ap_mac = db.Column(db.String(32), index=True)
    client_mac = db.Column(db.String(32), index=True)
    workspace = db.Column(db.String(256), index=True)

    stage = db.Column(db.Integer)
    tries = db.Column(db.Integer)

    def __repr__(self):
        return "<Auth {}>".format(self.ap_mac, self.client_mac)


class DataTransfer(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ap_mac = db.Column(db.String(32), index=True)
    client_mac = db.Column(db.String(32), index=True)
    workspace = db.Column(db.String(256), index=True)

    bytes = db.Column(db.Integer)

    def __repr__(self):
        return "<Transfer from {} to >".format(self.ap_mac, self.client_mac)


class Ap(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ap_mac = db.Column(db.String(32), index=True)
    workspace = db.Column(db.String(256), primary_key=True)

    mac_vendor = db.Column(db.String(256), nullable=True)
    essid = db.Column(db.String(256), index=True)
    channel = db.Column(db.Integer, index=True)
    privacy = db.Column(db.String(8), index=True)
    comment = db.Column(db.String(1024), nullable=True)

    def __repr__(self):
        return "<Ap {}:{}>".format(self.ap_mac, self.essid)


class Client(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    client_mac = db.Column(db.String(32), index=True)
    workspace = db.Column(db.String(256), primary_key=True)

    mac_vendor = db.Column(db.String(256), nullable=True)
    comment = db.Column(db.String(1024), nullable=True)

    def __repr__(self):
        return "<Client {}>".format(self.client_mac)


@login.user_loader
def load_user(user_id: int):
    return User.query.get(int(user_id))
