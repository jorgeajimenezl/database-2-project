import enum

from .. import db
from ..core.models import Model, Column, ForeignKey, PkModel, relationship


class Gender(enum.Enum):
    MALE = 1
    FEMALE = 2


class SchoolLevel(enum.Enum):
    PRIMARY = 1
    SECUNDARY = 2
    PRE_UNIVERSITARY = 3
    UNIVERSITARY = 4


class Employee(PkModel):
    __tablename__ = "Employees"

    phone = Column(db.String(20))
    name = Column(db.String(250), nullable=False, unique=True)
    gender = Column(db.Enum(Gender), nullable=False)
    school_level = Column(db.Enum(SchoolLevel), nullable=False)
    laboral_experience = Column(db.SmallInteger, nullable=False, default=0)
    address = Column(db.String(500))


class DriverType(enum.Enum):
    A = 0
    B = 1


class Driver(Model):
    __tablename__ = "Drivers"

    employee_id = Column(db.Integer, ForeignKey("Employees.id"), primary_key=True)
    type = Column(db.Enum(DriverType))
    evaluation = Column(db.SmallInteger, nullable=False, default=0)

    # Relation fields
    employee = relationship("Employee")

class Administrative(Model):
    __tablename__ = "Administratives"

    employee_id = Column(db.Integer, ForeignKey("Employees.id"), primary_key=True)
    position = Column(db.String(20), nullable=False)

    # Relation fields
    employee = relationship("Employee")

class Truck(Model):
    __tablename__ = "Trucks"

    id = Column(db.String(20), nullable=False, primary_key=True)
    weight = Column(db.Float, nullable=False, default=0.0)
    model = Column(db.String(20), nullable=False)
    fuel_type = Column(db.String(20), nullable=False)
    driver_id = Column(db.Integer, ForeignKey("Drivers.employee_id"))

    # Relation fields
    driver = relationship("Driver")

class LightweightTruck(Model):
    __tablename__ = "LightweightTrucks"

    truck_id = Column(db.String(20), ForeignKey("Trucks.id"), primary_key=True)
    max_speed = Column(db.Float, nullable=False, default=0.0)
    max_load = Column(db.Float, nullable=False, default=0.0)

    # Relation fields
    truck = relationship("Truck")


class HeavyTruck(Model):
    __tablename__ = "HeavyTrucks"

    truck_id = Column(db.String(20), ForeignKey("Trucks.id"), primary_key=True)
    spend_by_kilometer = Column(db.Float, nullable=False, default=0.0)
    length = Column(db.Float, nullable=False, default=0.0)
    width = Column(db.Float, nullable=False, default=0.0)
    height = Column(db.Float, nullable=False, default=0.0)
    # mileage = Column(db.Float, nullable=False, default=0.0)

    # Relation fields
    truck = relationship("Truck")

class Trip(PkModel):
    __tablename__ = "Trips"

    date = Column(db.Date, nullable=False)
    load = Column(db.Float, nullable=False, default=0.0)
    # mileage = Column(db.Float, nullable=False, default=0.0)
    destination = Column(db.String(200), nullable=False)
    truck_id = Column(db.String(20), ForeignKey("Trucks.id"), nullable=False)

    # Relation fields
    truck = relationship("Truck")

class InterprovincialTrip(Model):
    __tablename__ = "InterprovincialTrips"

    trip_id = Column(db.Integer, ForeignKey("Trips.id"), primary_key=True)
    return_date = Column(db.Date, nullable=True)
    # province_count = Column(db.SmallInteger, nullable=False, default=0)

    # Relation fields
    trip = relationship("Trip")
