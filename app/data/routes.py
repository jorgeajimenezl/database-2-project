from crypt import methods
from lib2to3.pgen2 import driver
from flask import flash, render_template

from .forms import TruckForm
from .models import Driver, Employee, Truck
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
            flash("Truck registration successful!!")
        else:
            flash("Invalid driver", "danger")

    return render_template("data/register_truck.html", form=form)

@data_bp.route("/register_employee", methods=["GET", "POST"])
def register_employee():
    pass