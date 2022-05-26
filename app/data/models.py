import enum
from re import A
from .. import db
from ..core.models import BaseMixin


class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"


class SchoolLevel(enum.Enum):
    PRIMARY = "primary"
    SECUNDARY = "secundary"
    PRE_UNIVERSITARY = "preuniversitary"
    UNIVERSITARY = "universitary"


class Employee(BaseMixin, db.Model):
    __tablename__ = "Employee"

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    school_level = db.Column(db.Enum(SchoolLevel), nullable=False)
    laboral_experience = db.Column(db.SmallInteger, nullable=False, default=0)
    address = db.Column(db.String(500))


class DriverType(enum.Enum):
    A = 0
    B = 1


class Driver(BaseMixin, db.Model):
    __tablename__ = "Driver"

    employee_id = db.Column(db.Integer, db.ForeignKey("Employee.id"))
    driver_type = db.Column(db.Enum(DriverType))
    evaluation = db.Column(db.SmallInteger, nullable=False, default=0)
    
    # Relation fields
    employee = db.relationship("Employee")
