"""
TEMPLATE - Use template to define how to generate a workout
UNDO/MOMENTO - UNDO ROUTES
FACTORY - Use a factory to generate routes.

"""
from Forms import LoginSignupForm, ClimberInfoForm, ClimberRouteForm, RouteTypes, HoldTypes
from flask import Flask, render_template, flash, request, abort, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, DecimalField, SelectMultipleField, IntegerField
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from flask.views import View
from enum import Enum

# Class Imports
from classes.Address import Address
from classes.ClimberInfo import ClimberInfo
from classes.Climber import Climber
from classes.RouteFactory import RouteFactory, BoulderingTypes
from classes.WorkoutStrategy import BeginnerWorkout, IntermediateWorkout, AdvancedWorkout
from classes.Workout import Workout

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config["MONGO_URI"] = "mongodb://localhost/Flash"
mongo = PyMongo(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class Gyms(Enum):
    locationsDictionary = mongo.db.Routes.find({}, {"location": 1, "_id": 0})
    locationsList = list(set([location["location"] for location in locationsDictionary]))
    locations = [(location, location) for location in locationsList]


class SkillLevel(Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"


class WorkoutForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=3, max=25), validators.DataRequired()])
    gym = SelectField('Gym', [validators.DataRequired()], choices=Gyms.locations.value)
    types = SelectMultipleField('Types', [validators.DataRequired()], choices=RouteTypes.routeTypes.value)
    holds = SelectMultipleField('Holds', [validators.DataRequired()], choices=HoldTypes.holdsTypes.value)
    numRoutes = IntegerField("NumberOfRoutes", [validators.DataRequired()])


@login_manager.user_loader
def load_climber(username):
    climber_info = mongo.db.ClimberInfo.find_one({"username": username})
    if climber_info is not None:

        firstname = climber_info["firstname"]
        lastname = climber_info["lastname"]
        street = climber_info["street"]
        city = climber_info["city"]
        state = climber_info["state"]
        zipCode = climber_info["zipCode"]
        phone_number = climber_info["phoneNumber"]
        favoriteGym = climber_info["favoriteGym"]
        skill_level = climber_info["climbingLevel"]

        address = Address(street, city, state, zipCode)
        climber_info_object = ClimberInfo(
            firstname, lastname, address, phone_number, skill_level)

        ############################################################################
        routes = mongo.db.Routes.find({"username": username})
        created_routes = []
        for route in routes:
            created_route = RouteFactory.createRoute(RouteFactory(), route["routeType"], route["routeName"], route["location"],
                                                     route["holds"], route["actualDifficulty"], route["feltDifficulty"])
            created_routes.append(created_route)
        ############################################################################

        climbers = mongo.db.Climbers.find_one({"username": username})
        username = username
        password = climbers["password"]

        return Climber(username, password, info=climber_info_object, favoriteGym=favoriteGym, routes=created_routes)


class LoginController(View):
    methods = ["GET", "POST"]

    def dispatch_request(self):
        form = LoginSignupForm()

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            climbers = mongo.db.Climbers
            found_climber = climbers.find_one(
                {"username": username, "password": password})

            if found_climber is not None:
                login_user(load_climber(found_climber["username"]))
                return redirect('climberRoutes')

            flash("Either the user doesn't exist or the password was incorrect.")
        return render_template('login.html', form=form)


class LogoutController(View):
    methods = ["GET", "POST"]

    def dispatch_request(self):
        logout_user()
        flash('You are now logged out.', 'success')
        return redirect('login')


class SignupController(View):
    methods = ["GET", "POST"]

    def dispatch_request(self):
        form = LoginSignupForm()

        if form.validate_on_submit():
            if self.update_database(form):
                return render_template("login.html", form=form)

            flash('That username already exists!')
        return render_template('signup.html', form=form)

    def update_database(self, form):
        success = False

        username = form.username.data
        password = form.password.data

        existing_user = mongo.db.Climbers.find_one({"username": username})

        if existing_user is None:
            mongo.db.Climbers.insert(
                {'username': username, 'password': password})
            info_attributes = ['firstname', 'lastname', "street", "city",
                               "state", "zipCode", 'phoneNumber', 'favoriteGym', 'climbingLevel']

            climber_info_dict = {'username': username}
            for attribte in info_attributes:
                climber_info_dict[attribte] = ""

            mongo.db.ClimberInfo.insert(climber_info_dict)

            success = True

        return success


class ClimberInfoController(View):
    methods = ["GET", "POST"]
    decorators = [login_required]

    def dispatch_request(self):
        form = ClimberInfoForm()

        if form.validate_on_submit():
            if self.update_database(form):
                flash("Succesfully updated info.")
                form = ClimberInfoForm()

                return redirect(url_for('climberInfo', form=form))

            flash("Error when updating info.")
        return render_template('climberInfo.html', form=form)

    def update_database(self, form):
        success = False

        climber_info = mongo.db.ClimberInfo
        for element in form:
            if len(element.data) > 0:
                climber_info.update({"username": current_user.getUsername()}, {
                                    "$set": {element.id: element.data}})

        success = True
        return success


class ClimberRouteController(View):
    methods = ["GET", "POST"]
    decorators = [login_required]

    def dispatch_request(self):
        form = ClimberRouteForm()

        if form.validate_on_submit():
            if self.update_database(form):
                flash("Successfully added route.")
                return redirect(url_for('climberRoutes', form=form, ))

            flash("Route Name is taken already.")
            form = ClimberRouteForm()
        return render_template('climberRoutes.html', form=form)

    def update_database(self, form):
        success = False
        if not mongo.db.Routes.find_one({"routeName": form.routeName.data}):
            routes_dict = {"username": current_user.getUsername()}

            for element in form:
                routes_dict[element.id] = element.data
            mongo.db.Routes.insert(routes_dict)

            success = True

        return success

class workoutGeneratorController(View):
    methods = ["GET", "POST"]
    decorators = [login_required]

    def dispatch_request(self):
        form = WorkoutForm()

        if form.validate_on_submit():
            routes = list(mongo.db.Routes.find({"location": form.gym.data}))
            workout = Workout(routes, form, self.determine_workout_strategy())
            return render_template('generateWorkout.html', form=form, workout=workout)

        return render_template('generateWorkout.html', form=form)

    def determine_workout_strategy(self):
        if current_user.getInfo().getSkillLevel() == SkillLevel.beginner.value:
            return BeginnerWorkout()
        elif current_user.getInfo().getSkillLevel() == SkillLevel.intermediate.value:
            return IntermediateWorkout()
        elif current_user.getInfo().getSkillLevel() == SkillLevel.advanced.value:
            return AdvancedWorkout()


app.add_url_rule('/login', view_func=LoginController.as_view('login'))
app.add_url_rule('/logout', view_func=LogoutController.as_view('logout'))
app.add_url_rule('/signup', view_func=SignupController.as_view('signup'))
app.add_url_rule('/climberInfo', view_func=ClimberInfoController.as_view('climberInfo'))
app.add_url_rule('/climberRoutes', view_func=ClimberRouteController.as_view('climberRoutes'))
app.add_url_rule('/generateWorkout', view_func=workoutGeneratorController.as_view('generateWorkout'))


@app.route('/index')
@login_required
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)