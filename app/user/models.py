from enum import unique
from ipaddress import ip_address
from authlib.jose import JsonWebToken
from datetime import datetime
from flask import current_app, request
from flask_login import UserMixin, login_user, logout_user
from sqlalchemy import desc

from .. import db, login_manager, bcrypt
from ..core.models import PkModel, Column, relationship, ForeignKey


class Role(PkModel):
    __tablename__ = "Roles"

    name = Column(db.String(20), nullable=False, unique=True)
    description = Column(db.String(200))


class UserAccount(PkModel, UserMixin):
    __tablename__ = "Users"

    email = Column(db.String(100), nullable=False, unique=True)
    password = Column(db.Text, nullable=False)
    is_verified = Column(db.Boolean, default=False)
    last_active = Column(db.DateTime)
    role_id = Column(db.Integer, ForeignKey("Roles.id"), nullable=False)

    # Relation fields
    role = relationship("Role")

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
