import enum

from sqlalchemy import nullslast
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

    phone = Column(db.String(20))
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
    type = Column(db.Enum(DriverType))
    evaluation = Column(db.SmallInteger, nullable=False, default=0)

    # Relation fields
    employee = relationship("Employee")

class Administrative(Model):
    __tablename__ = "Administrative"

    employee_id = Column(db.Integer, ForeignKey("Employee.id"), primary_key=True)
    position = Column(db.String(20), nullable=False)

    # Relation fields
    employee = relationship("Employee")

class Truck(PkModel):
    __tablename__ = "Truck"

    weight = Column(db.Float, nullable=False, default=0.0)
    model = Column(db.String(20), nullable=False)
    fuel_type = Column(db.String(20), nullable=False)
    driver_id = Column(db.Integer, ForeignKey("Driver.employee_id"))

    # Relation fields
    driver = relationship("Driver")

class LightweightTruck(Model):
    __tablename__ = "LightweightTruck"

    truck_id = Column(db.Integer, ForeignKey("Truck.id"), primary_key=True)
    max_speed = Column(db.Float, nullable=False, default=0.0)
    max_load = Column(db.Float, nullable=False, default=0.0)

    # Relation fields
    truck = relationship("Truck")


class HeavyTruck(Model):
    __tablename__ = "HeavyTruck"

    truck_id = Column(db.Integer, ForeignKey("Truck.id"), primary_key=True)
    spend_by_kilometer = Column(db.Float, nullable=False, default=0.0)
    length = Column(db.Float, nullable=False, default=0.0)
    width = Column(db.Float, nullable=False, default=0.0)
    height = Column(db.Float, nullable=False, default=0.0)
    # mileage = Column(db.Float, nullable=False, default=0.0)

    # Relation fields
    truck = relationship("Truck")

class Trip(PkModel):
    __tablename__ = "Trip"

    date = Column(db.Date, nullable=False)
    load = Column(db.Float, nullable=False, default=0.0)
    mileage = Column(db.Float, nullable=False, default=0.0)
    truck_id = Column(db.Integer, ForeignKey("Truck.id"))

    # Relation fields
    truck = relationship("Truck")

class InterprovincialTrip(Model):
    __tablename__ = "InterprovincialTrip"

    trip_id = Column(db.Integer, ForeignKey("Trip.id"), primary_key=True)
    return_date = Column(db.Date, nullable=True)
    province_count = Column(db.SmallInteger, nullable=False, default=0)

    # Relation fields
    trip = relationship("Trip")
