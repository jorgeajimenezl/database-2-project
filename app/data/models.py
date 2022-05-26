import enum
from .. import db
from ..core.models import Model, Column, ForeignKey, PkModel, relationship


class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"


class SchoolLevel(enum.Enum):
    PRIMARY = "primary"
    SECUNDARY = "secundary"
    PRE_UNIVERSITARY = "preuniversitary"
    UNIVERSITARY = "universitary"


class Employee(PkModel):
    __tablename__ = "Employee"

    phone = Column(db.String)
    name = Column(db.String(250), nullable=False)
    gender = Column(db.Enum(Gender), nullable=False)
    school_level = Column(db.Enum(SchoolLevel), nullable=False)
    laboral_experience = Column(db.SmallInteger, nullable=False, default=0)
    address = Column(db.String(500))


class DriverType(enum.Enum):
    A = 0
    B = 1


class Driver(Model):
    __tablename__ = "Driver"

    employee_id = Column(db.Integer, ForeignKey("Employee.id"), primary_key=True)
    driver_type = Column(db.Enum(DriverType))
    evaluation = Column(db.SmallInteger, nullable=False, default=0)

    # Relation fields
    employee = relationship("Employee")
