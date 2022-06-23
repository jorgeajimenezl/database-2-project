from flask_wtf import FlaskForm
from pymysql import Date
from traitlets import default
from wtforms import (
    ValidationError,
    StringField,
    DecimalField,
    SelectField,
    IntegerField,
    DateField,
    BooleanField,
)
from wtforms.validators import (
    DataRequired,
    EqualTo,
    NumberRange,
    Regexp,
    StopValidation,
)

# import phonenumbers

from .models import DriverType, Gender, InterprovincialTrip, SchoolLevel


class DependsOf:
    def __init__(self, fields: dict, extra_validators=[], message=None):
        self.message = message
        self.fields = fields
        self.extra_validators = extra_validators

    def __call__(self, form, field):
        for k, v in self.fields.items():
            if hasattr(form, k) and getattr(form, k).data != v:
                return

        for validator in self.extra_validators:
            validator(form, field)
        return


class RegisterTruckForm(FlaskForm):
    id = StringField("ID", validators=[DataRequired()])
    model = StringField("Model", validators=[DataRequired()])
    weight = DecimalField("Weight", validators=[DataRequired()])
    fuel_type = SelectField(
        "Fuel Type", choices=["Gasoline", "Diesel"], validators=[DataRequired()]
    )
    driver = SelectField("Driver", validators=[DataRequired()])
    truck_type = SelectField(
        "Type", validators=[DataRequired()], choices=["Lightweight", "Heavy"]
    )

    # Lightweight truck fields
    max_speed = DecimalField(
        "Max. Speed",
        validators=[
            DependsOf(
                {"truck_type": "Lightweight"},
                extra_validators=[DataRequired(), NumberRange(min=0)],
            )
        ],
        default=0,
    )
    max_load = DecimalField(
        "Max. Load",
        validators=[
            DependsOf(
                {"truck_type": "Lightweight"},
                extra_validators=[DataRequired(), NumberRange(min=0)],
            )
        ],
        default=0,
    )

    # Heavy truck fields
    spend_by_kilometer = DecimalField(
        "Spend by Km.",
        validators=[
            DependsOf(
                {"truck_type": "Heavy"},
                extra_validators=[DataRequired(), NumberRange(min=0)],
            )
        ],
        default=0,
    )
    length = DecimalField(
        "Length",
        validators=[
            DependsOf(
                {"truck_type": "Heavy"},
                extra_validators=[DataRequired(), NumberRange(min=0)],
            )
        ],
        default=0,
    )
    width = DecimalField(
        "Width",
        validators=[
            DependsOf(
                {"truck_type": "Heavy"},
                extra_validators=[DataRequired(), NumberRange(min=0)],
            )
        ],
        default=0,
    )
    height = DecimalField(
        "Height",
        validators=[
            DependsOf(
                {"truck_type": "Heavy"},
                extra_validators=[DataRequired(), NumberRange(min=0)],
            )
        ],
        default=0,
    )


class RegisterEmployeeForm(FlaskForm):
    phone = StringField(
        "Phone",
        validators=[
            DataRequired(),
            Regexp(
                "\+?(53)? *5\d{7}",
                message="The phone must be a valid Cuban phone number. Ex: +53 55776611",
            ),
        ],
    )
    name = StringField("Name", validators=[DataRequired()])
    gender = SelectField(
        "Gender",
        validators=[DataRequired()],
        # coerce=Gender,
        choices=[x.name.replace("_", " ").capitalize() for x in Gender],
    )
    school_level = SelectField(
        "School level",
        validators=[DataRequired()],
        # coerce=SchoolLevel,
        choices=[x.name.replace("_", " ").capitalize() for x in SchoolLevel],
    )
    laboral_experience = IntegerField(
        "Laboral experience",
        validators=[
            NumberRange(
                min=0,
                message="The laboral experience must be a positive integer in years",
            )
        ],
    )
    address = StringField("Address", validators=[DataRequired()])
    employee_type = SelectField(
        "Type", validators=[DataRequired()], choices=["Driver", "Administrative"]
    )

    # Driver fields
    driver_type = SelectField(
        "Driver type",
        validators=[
            DependsOf({"employee_type": "Driver"}, extra_validators=[DataRequired()])
        ],
        choices=[x.name.replace("_", " ").capitalize() for x in DriverType],
    )
    driver_evaluation = IntegerField(
        "Driver evaluation",
        validators=[
            DependsOf(
                {"employee_type": "Driver"},
                extra_validators=[DataRequired(), NumberRange(min=0)],
            ),
        ],
        default=0,
    )

    # Administrative fields
    administrative_position = StringField(
        "Administrative position",
        validators=[
            DependsOf(
                {"employee_type": "Administrative"}, extra_validators=[DataRequired()]
            )
        ],
    )


class RegisterTripForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    load = DecimalField(
        "Load", validators=[DataRequired(), NumberRange(min=0)], default=0
    )
    destination = StringField("Destination", validators=[DataRequired()])
    truck = SelectField("Truck", validators=[DataRequired()])

    is_interprovincial = BooleanField("Is interprovincial?", default=False)
    return_date = DateField(
        "Return date",
        validators=[
            DependsOf({"is_interprovincial": True}, extra_validators=[DataRequired()])
        ],
    )
