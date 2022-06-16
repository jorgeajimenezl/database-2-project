import re
from flask import flash, render_template

from .forms import EmployeeForm, TruckForm
from .models import Administrative, Driver, Employee, Gender, SchoolLevel, Truck
from ..auth import login_required
from . import data_bp


@data_bp.route("/register_truck", methods=["GET", "POST"])
def register_truck():
    form = TruckForm()
    drivers = Driver.query.all()
    form.driver.choices = {x.employee.name: x.employee_id for x in drivers}

    if form.validate_on_submit():
        employee = Employee.get_by_id(form.driver.data)
        if employee:
            Truck.create(
                weight=float(form.weight.data),
                model=form.model.data,
                fuel_type=form.model.data,
                driver_id=form.driver.data,
            )
            flash("Truck registration successfull!!", "success")
        elif form.is_submitted():
            flash("Invalid driver data", "danger")

    return render_template("data/register_truck.html", form=form)


@data_bp.route("/register_employee", methods=["GET", "POST"])
def register_employee():
    form = EmployeeForm()

    if form.validate_on_submit():
        # Normalize phone number
        phone = re.match("\+?(53)? *(5\d{7})", form.phone.data)

        e = Employee.create(
            phone=f"+53 {phone[2]}",
            name=form.name.data,
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
                employee_id=e.id,
                position=form.administrative_position.data
            )
            
            flash("Administrative registration successfull!!", "success")
    elif form.is_submitted():
        flash("Invalid employee data", "danger")

    return render_template("data/register_employee.html", form=form)
