from ipaddress import ip_address
from authlib.jose import JsonWebToken
from datetime import datetime
from flask import current_app, request
from flask_login import UserMixin, login_user, logout_user
from sqlalchemy import desc

from .. import db, login_manager, bcrypt
from ..core.models import BaseMixin


class UserAccount(BaseMixin, UserMixin, db.Model):
    __tablename__ = "Users"

    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    last_active = db.Column(db.DateTime)

    def set_new_password(self, passwd):
        self.update(
            password=bcrypt.generate_password_hash(passwd).decode("utf-8"),
        )
        db.session.commit()

    def get_token(self):
        jwt = JsonWebToken(["RS256"])
        return jwt.encode(
            header={"alg": "RS256"},
            payload={
                "user_id": self.id,
                "exp": int(
                    (
                        datetime.utcnow() + current_app.config["PWD_RESET_EXP"]
                    ).timestamp()
                ),
            },
            key=current_app.config["JWT_PRIVATE_KEY"],
        )

    @classmethod
    def verify_token(cls, token):
        jwt = JsonWebToken(["RS256"])
        claims = jwt.decode(token, current_app.config["JWT_PUBLIC_KEY"])
        try:
            claims.validate()
        except Exception as err:
            current_app.logger.debug(err)
            return None
        else:
            return cls.query.filter_by(id=claims["user_id"]).first()


@login_manager.user_loader
def user_loader(user_id):
    return UserAccount.query.get(int(user_id))
