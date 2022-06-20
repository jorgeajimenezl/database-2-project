import click
from flask import current_app, url_for
from flask.cli import AppGroup
from sqlalchemy.exc import IntegrityError
from getpass import getpass

from .models import Role, UserAccount
from .. import bcrypt, db
from ..auth.utils import validate_password

user_cli = AppGroup("user", help="Manage user data")


@user_cli.command("create")
@click.argument("email")
@click.argument("role")
@click.option(
    "--verified", "-v", is_flag=True, help="True to set the user verified flag to on"
)
def create_user(email: str, role: str, verified: bool):
    user = UserAccount.query.filter_by(email=email).first()
    if user:
        raise Exception("Email already taken")

    role = Role.query.filter_by(name=role).first()
    if not role:
        raise Exception("Role name doesn't exists")

    password = getpass("Enter user password: ")
    if not validate_password(password):
        continue_ = input(
            "Password does not meet security requirements. Would you like to continue? [y/N]: "
        )
        if not continue_.lower().startswith("y"):
            raise Exception("Password invalid.")
    if password != getpass("Retype the password: "):
        raise Exception("Passwords don't match")

    user = UserAccount(
        email=email,
        password=bcrypt.generate_password_hash(password).decode("utf-8"),
        is_verified=verified,
        role_id=role.id,
    )

    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        raise Exception("Could not add user.")
    else:
        current_app.logger.info("User Added!")


@user_cli.command("create_role")
@click.argument("name")
@click.argument("description", required=False)
def create_role(name: str, description: str = None):
    if Role.query.filter_by(name=name).first():
        raise Exception("Name already exists")
    
    role = Role(name=name, description=description)
    db.session.add(role)
    try:
        db.session.commit()
    except IntegrityError:
        raise Exception("Could not add role.")
    else:
        current_app.logger.info("Role Added!")

@user_cli.command("password_reset")
@click.argument("email")
def password_reset(email: str):
    user = UserAccount.query.filter_by(email=email).first()
    if not user:
        raise Exception("User not found")

    url = url_for("auth.password_reset", token=user.get_token(), _external=True)
    current_app.logger.info(url)
