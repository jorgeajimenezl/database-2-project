import re
from typing import List

from flask import flash, render_template

from ..auth import login_required
from . import data_bp
from .forms import EmployeeForm, TruckForm
from .models import (
    Administrative,
    Driver,
    Employee,
    Gender,
    HeavyTruck,
    LightweightTruck,
    SchoolLevel,
    Truck,
)


@data_bp.route("/register/truck", methods=["GET", "POST"])
def register_truck():
    form = TruckForm()
    drivers: List[Driver] = Driver.query.all()
    form.driver.choices = [x.employee.name for x in drivers]

    if form.validate_on_submit():
        index = -1
        for i in drivers:
            if i.employee.name == form.driver.data:
                index = i.employee_id

        if index != -1:
            t = Truck.create(
                weight=float(form.weight.data),
                model=form.model.data,
                fuel_type=form.fuel_type.data,
                driver_id=index,
            )

            if form.truck_type.data == "Lightweight":
                LightweightTruck.create(
                    truck_id=t.id,
                    max_speed=float(form.max_speed.data),
                    max_load=float(form.max_load.data),
                )
                flash("Lightweight truck registration successfull!!", "success")
            else:
                HeavyTruck.create(
                    truck_id=t.id,
                    spend_by_kilometer=float(form.spend_by_kilometer.data),
                    length=float(form.length.data),
                    width=float(form.width.data),
                    height=float(form.height.data),
                )
                flash("Heavy truck registration successfull!!", "success")
        elif form.is_submitted():
            flash("Invalid driver data", "danger")

    return render_template("data/register_truck.html", form=form)


@data_bp.route("/manage/employee")
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
def register_employee():
    form = EmployeeForm()

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
        else:
            Administrative.create(
                employee_id=e.id, position=form.administrative_position.data
            )

            flash("Administrative registration successfull!!", "success")
    elif form.is_submitted():
        flash("Invalid employee data", "danger")

    return render_template("data/register_employee.html", form=form)
