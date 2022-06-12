from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, FloatField, SelectField
from wtforms.validators import DataRequired, EqualTo

class TruckForm(FlaskForm):
    model = StringField("Model", validators=[DataRequired()])
    weight = FloatField("Weight", validators=[DataRequired()])
    fuel_type = SelectField("Fuel Type", choices=["Gasoline", "Diesel"], validators=[DataRequired()])

    
    

    
