import itertools
import re
import itertools
from typing import List

from flask import flash, redirect, render_template, url_for
from sqlalchemy import func, select

from ..auth import login_required, role_required
from . import data_bp
from .. import db
from .forms import RegisterEmployeeForm, RegisterTripForm, RegisterTruckForm
from .models import (
    Administrative,
    Driver,
    Employee,
    Gender,
    HeavyTruck,
    InterprovincialTrip,
    LightweightTruck,
    SchoolLevel,
    Trip,
    Truck,
)


@data_bp.route("/register/truck", methods=["GET", "POST"])
@role_required(["Administrator", "Manager"])
def register_truck():
    form = RegisterTruckForm()
    drivers: List[Driver] = Driver.query.all()
    form.driver.choices = [x.employee.name for x in drivers]

    if form.validate_on_submit():
        index = -1
        for i in drivers:
            if i.employee.name == form.driver.data:
                index = i.employee_id

        if index != -1:
            Truck.create(
                id=form.id.data,
                weight=float(form.weight.data),
                model=form.model.data,
                fuel_type=form.fuel_type.data,
                driver_id=index,
            )

            if form.truck_type.data == "Lightweight":
                LightweightTruck.create(
                    truck_id=form.id.data,
                    max_speed=float(form.max_speed.data),
                    max_load=float(form.max_load.data),
                )
                flash("Lightweight truck registration successfull!!", "success")
            else:
                HeavyTruck.create(
                    truck_id=form.id.data,
                    spend_by_kilometer=float(form.spend_by_kilometer.data),
                    length=float(form.length.data),
                    width=float(form.width.data),
                    height=float(form.height.data),
                )
                flash("Heavy truck registration successfull!!", "success")

            return redirect(url_for("data.manage_truck"))
        elif form.is_submitted():
            flash("Invalid driver data", "danger")

    return render_template("data/register_truck.html", form=form)


@data_bp.route("/manage/employee")
@role_required(["Administrator", "Manager"])
def manage_employee():
    headers = [
        "ID",
        "Name",
        "Phone",
        "Gender",
        "School level",
        "Laboral experience",
        "Address",
    ]
    administratives_headers = headers + ["Position"]
    drivers_headers = headers + ["Driver type", "Evaluation"]

    administratives_data = Administrative.query.all()
    drivers_data = Driver.query.all()

    def get_data(e: Employee):
        return [
            e.id,
            e.name,
            e.phone,
            str(e.gender.name).capitalize(),
            str(e.school_level.name).capitalize().replace("_", " "),
            f"{e.laboral_experience} years",
            e.address,
        ]

    return render_template(
        "data/manage_employee.html",
        administratives_headers=administratives_headers,
        administratives_data=list(
            map(lambda x: get_data(x.employee) + [x.position], administratives_data)
        ),
        drivers_headers=drivers_headers,
        drivers_data=list(
            map(
                lambda x: get_data(x.employee) + [x.type.name, x.evaluation],
                drivers_data,
            )
        ),
    )


@data_bp.route("/manage/truck")
@role_required(["Administrator", "Manager"])
def manage_truck():
    headers = [
        "ID",
        "Weight",
        "Model",
        "Fuel type",
    ]
    lightweight_headers = headers + ["Max. Speed", "Max. Load"]
    heavy_headers = headers + ["Spend/Km.", "Length", "Width", "Height"]

    lightweight_data = LightweightTruck.query.all()
    heavy_data = HeavyTruck.query.all()

    def get_data(t: Truck):
        return [
            t.id,
            t.weight,
            t.model,
            str(t.fuel_type).capitalize(),
        ]

    return render_template(
        "data/manage_truck.html",
        lightweight_headers=lightweight_headers,
        lightweight_data=list(
            map(
                lambda x: get_data(x.truck) + [x.max_speed, x.max_load],
                lightweight_data,
            )
        ),
        heavy_headers=heavy_headers,
        heavy_data=list(
            map(
                lambda x: get_data(x.truck)
                + [x.spend_by_kilometer, x.length, x.width, x.height],
                heavy_data,
            )
        ),
    )


@data_bp.route("/register/employee", methods=["GET", "POST"])
@role_required(["Administrator", "Manager"])
def register_employee():
    form = RegisterEmployeeForm()

    if form.validate_on_submit():
        # Normalize phone number
        phone = re.match("\+?(53)? *(5\d{7})", form.phone.data)
        # Normalize name
        name = str.join(" ", map(str.capitalize, form.name.data.split()))

        e = Employee.create(
            phone=f"+53 {phone[2]}",
            name=name,
            gender=Gender[form.gender.data.replace(" ", "_").upper()],
            school_level=SchoolLevel[form.school_level.data.replace(" ", "_").upper()],
            laboral_experience=form.laboral_experience.data,
            address=form.address.data,
        )
        if form.employee_type.data == "Driver":
            Driver.create(
                employee_id=e.id,
                type=form.driver_type.data,
                evaluation=form.driver_evaluation.data,
            )

            flash("Driver registration successfull!!", "success")
        elif form.employee_type.data == "Administrative":
            Administrative.create(
                employee_id=e.id, position=form.administrative_position.data
            )

            flash("Administrative registration successfull!!", "success")
        else:
            flash("Employee registration successfull!!", "success")

        return redirect(url_for("data.manage_employee"))
    elif form.is_submitted():
        flash("Invalid employee data", "danger")

    return render_template("data/register_employee.html", form=form)


@data_bp.route("/register/trip", methods=["GET", "POST"])
@login_required()
def register_trip():
    form = RegisterTripForm()
    trucks: List[Truck] = Truck.query.all()
    form.truck.choices = [x.id for x in trucks]

    if form.validate_on_submit():
        if not any(map(lambda x: x.id == form.truck.data, trucks)):
            flash("Invalid driver data", "danger")
        else:
            t = Trip.create(
                date=form.date.data,
                load=float(form.load.data),
                destination=form.destination.data,
                truck_id=form.truck.data,
            )

            if form.is_interprovincial.data:
                InterprovincialTrip.create(
                    trip_id=t.id, return_date=form.return_date.data
                )

            flash("Successfull trip register", "success")
            return redirect(url_for("data.manage_trip"))

    return render_template("data/register_trip.html", form=form)


@data_bp.route("/manage/trip")
@login_required()
def manage_trip():
    trips = Trip.query.all()

    def get_data(x: Trip):
        i = InterprovincialTrip.query.filter_by(trip_id=x.id).first()
        return [
            x.id,
            x.destination,
            x.date,
            x.load,
            bool(i),
            x.truck_id,
            i.return_date if i else "-",
        ]

    return render_template(
        "data/manage_trip.html",
        trips_headers=[
            "ID",
            "Destination",
            "Date",
            "Load",
            "Interprovincial?",
            "Truck id",
            "Return date",
        ],
        trips_data=list(map(get_data, trips)),
    )


@data_bp.route("/generate-paysheet")
@role_required(["Administrator", "Manager"])
def generate_paysheet():
    def get_data():
        return itertools.chain(
            (
                db.session.query(
                    Employee.name,
                    func.count(Trip.id) * 30 + 4500,
                )
                .join(InterprovincialTrip.trip)
                .join(Trip.truck)
                .join(Truck.driver)
                .join(Driver.employee)
                .filter(Driver.type == "A")
                .group_by(Driver.employee_id)
                .all()
            ),
            (
                db.session.query(Employee.name, 10 * Driver.evaluation + 4500)
                .join(Driver.employee)
                .filter(Driver.type == "B")
                .all()
            ),
            (db.session.query(Employee.name, 4700).join(Administrative.employee).all()),
            (
                db.session.query(Employee.name, 4500).filter(
                    Employee.id.not_in(select(Driver.employee_id)),
                    Employee.id.not_in(select(Administrative.employee_id)),
                )
            ),
        )

    return render_template(
        "data/paysheet.html", headers=["Name", "Salary (USD)"], employees=get_data()
    )


@data_bp.route("/statistics/trucks")
@login_required()
def statistics_trucks():
    return render_template("data/statistics_trucks.html")
