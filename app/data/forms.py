from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, DecimalField, SelectField
from wtforms.validators import DataRequired, EqualTo, NumberRange

class TruckForm(FlaskForm):
    model = StringField("Model", validators=[DataRequired()])
    weight = DecimalField("Weight", validators=[DataRequired()])
    fuel_type = SelectField("Fuel Type", choices=["Gasoline", "Diesel"], validators=[DataRequired()])
    driver = SelectField("Driver", validators=[DataRequired()])
    
    

    
