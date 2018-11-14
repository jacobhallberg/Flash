from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, DecimalField, SelectMultipleField
from enum import Enum

class HoldTypes(Enum):
    holdTypesList = ["Crimpy", "Jugs", "Edges", "Pinch", "Sloper", "Pocket", "Undercling", "Flake", "Horn"]
    holdsTypes = [(hold, hold) for hold in holdTypesList]

class RouteTypes(Enum):
    routeTypesList = ["Boulder", "Lead", "TopRope"]
    routeTypes = [(routeType, routeType) for routeType in routeTypesList]

class ClimbingLevels(Enum):
    climbingLevelsList = ["Beginner", "Intermediate", "Advanced"]
    climbingLevels = [(level, level) for level in climbingLevelsList]

class LoginSignupForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=3, max=25), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class ClimberInfoForm(FlaskForm):
    firstname = StringField('Firstname')
    lastname = StringField('Lastname')
    street = StringField('Street')
    city = StringField('City')
    state = StringField('State')
    zipCode = StringField('ZipCode')
    phoneNumber = StringField('PhoneNumber')
    favoriteGym = StringField('FavoriteGym')

    climbingLevel =  SelectField('ClimbingLevel', [validators.DataRequired()], choices=ClimbingLevels.climbingLevels.value)

class ClimberRouteForm(FlaskForm):
    routeName = StringField('RouteName', [validators.DataRequired()])
    routeType = SelectField('RouteType', [validators.DataRequired()], choices=RouteTypes.routeTypes.value)

    location = StringField('Location', [validators.DataRequired()])
    holds = SelectMultipleField('Holds', [validators.DataRequired()], choices=HoldTypes.holdsTypes.value)

    actualDifficulty = StringField('ActualDifficulty', [validators.DataRequired()])
    feltDifficulty = StringField('FeltDifficulty', [validators.DataRequired()])


