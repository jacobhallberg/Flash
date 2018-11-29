from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, DecimalField, SelectMultipleField
from enum import Enum

class HoldTypes(Enum):
    """ Enum holding the hold types in the format needed by Flask forms. 
    """
    holdTypesList = ["Crimpy", "Jugs", "Edges", "Pinch", "Sloper", "Pocket", "Undercling", "Flake", "Horn"]
    hold_types = [(hold, hold) for hold in holdTypesList]

class RouteTypes(Enum):
    """ Enum holding the route types in the format needed by Flask forms.
    """
    route_typesList = ["Bouldering", "Lead", "TopRope"]
    route_types = [(route_type, route_type) for route_type in route_typesList]

class ClimbingLevels(Enum):
    """ Enum holding the climbing levels in the format needed by Flask forms.
    """
    climbingLevelsList = ["Beginner", "Intermediate", "Advanced"]
    climbing_levels = [(level, level) for level in climbingLevelsList]

class LoginSignupForm(FlaskForm):
    """ FlaskForm subclass defining the needed fields to login.
    """
    username = StringField('Username', [validators.Length(min=3, max=25), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class ClimberInfoForm(FlaskForm):
    """ FlaskForm subclass defining the needed fields to add information to
        the ClimberInfo object.
    """
    firstname = StringField('Firstname')
    lastname = StringField('Lastname')
    street = StringField('Street')
    city = StringField('City')
    state = StringField('State')
    zip_code = StringField('zip_code')
    phone_number = StringField('phone_number')

    climbingLevel =  SelectField('ClimbingLevel', [validators.DataRequired()], choices=ClimbingLevels.climbing_levels.value)

class ClimberRouteForm(FlaskForm):
    """ FlaskForm subclass defining the needed fields to create a route.
    """
    route_name = StringField('route_name', [validators.DataRequired()])
    route_type = SelectField('route_type', [validators.DataRequired()], choices=RouteTypes.route_types.value)

    location = StringField('Location', [validators.DataRequired()])
    holds = SelectMultipleField('Holds', [validators.DataRequired()], choices=HoldTypes.hold_types.value)

    actual_difficulty = StringField('actual_difficulty', [validators.DataRequired()])
    felt_difficulty = StringField('felt_difficulty', [validators.DataRequired()])


