"""
TEMPLATE - Use template to define how to generate a workout
UNDO/MOMENTO - UNDO ROUTES
FACTORY - Use a factory to generate routes.

"""
from flask import Flask, render_template, flash, request, abort, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, DecimalField, SelectMultipleField, IntegerField, FloatField
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from flask.views import View
from enum import Enum

# Class Imports
from classes.Address import Address
from classes.ClimberInfo import ClimberInfo
from classes.Climber import Climber
from classes.RouteFactory import RouteFactory, ClimbingTypes
from classes.WorkoutStrategy import BeginnerWorkout, IntermediateWorkout, AdvancedWorkout
from classes.Workout import Workout
from classes.Hold import BaseHold, DecoratorHold
from Forms import LoginSignupForm, ClimberInfoForm, ClimberRouteForm, RouteTypes, HoldTypes


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config["MONGO_URI"] = "mongodb://localhost/Flash"
mongo = PyMongo(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class Gyms(Enum):
    """ Enum holding the locations in the format needed by Flask forms.
    """
    locationsDictionary = mongo.db.Routes.find({}, {"location": 1, "_id": 0})
    locationsList = list(set([location["location"] for location in locationsDictionary]))
    locations = [(location, location) for location in locationsList]

class SkillLevel(Enum):
    """ Enum holding the possible climber skill levels.
    """
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"

class WorkoutForm(FlaskForm):
    """ Form containing the neccesary parameters to generate a workout.
    """
    name = StringField('Name', [validators.Length(min=3, max=25), validators.DataRequired()])
    gym = SelectField('Gym', [validators.DataRequired()], choices=Gyms.locations.value)
    types = SelectMultipleField('Types', [validators.DataRequired()], choices=RouteTypes.route_types.value)
    holds = SelectMultipleField('Holds', [validators.DataRequired()], choices=HoldTypes.hold_types.value)
    numRoutes = FloatField("NumberOfRoutes", [validators.DataRequired()])

def load_climber_info_object(climber_info):
    """ Creates a ClimberInfo object with data stored in the Mongo DB.
    Parameters
    ----------
    climber_info (dict): Information grabbed from a specific climber
                            stored in the Mongo DB.
    Returns
    -------
    ClimberInfo (ClimberInfo): A climber info object with all of the neccesary
                                fields grabbed from the Mongo DB.
    """
    firstname = climber_info["firstname"]
    lastname = climber_info["lastname"]
    street = climber_info["street"]
    city = climber_info["city"]
    state = climber_info["state"]
    zip_code = climber_info["zip_code"]
    phone_number = climber_info["phone_number"]
    skill_level = climber_info["climbingLevel"]

    address = Address(street, city, state, zip_code)
    return ClimberInfo(firstname, lastname, address, phone_number, skill_level)

def load_holds(_holds):
    """ Makes use of the decorator design pattern by chain creating hold objects.
        If the length of holds is greater than 1 it creates a decorator hold object
        containing all holds as an individual object stored in a bigger decorator object.
    Parameters
    ----------
    holds (list<str>): Holds returned from the Mongo DB.

    Returns
    -------
    holds (Hold): Returns a hold object consisting of all of the holds found
                    on an individual route.
    """
    holds = BaseHold(_holds[0])
    
    if len(_holds) >= 2:
        for hold in _holds[1:]:
            holds = DecoratorHold(hold, holds)

    return holds

def load_routes(username):
    """ Given a username this function loads all of the routes stored in a 
        Mongo DB and returns a list of Route objects.
    Parameters
    ----------
    username (str): The username of the climber.

    Returns
    -------
    loaded_routes (list<Route>): All of the route associated with a specific climber.
    """
    routes = mongo.db.Routes.find({"username": username})
    loaded_routes = []

    for route in routes:
        created_route = RouteFactory.create_route(
            RouteFactory(
            ), route["route_type"], route["route_name"], route["location"],
            load_holds(route["holds"]), route["actual_difficulty"], route["felt_difficulty"]
        )
        loaded_routes.append(created_route)
    return loaded_routes

@login_manager.user_loader
def load_climber(username):
    """ Makes use of Flask login to ensure that the current username is logged in
        when using pages that have the login_required requirement. Additionally, loads
        a Climber object with the specific information by loading all of the information
        from the Mongo DB.
    Parameters
    ----------
    username (str): The username of the climber.

    Returns
    -------
    Climber (Climber): Returns a climber object with its username, personal info,
                        and all of the routes created by that climber.
    """
    climber_info = mongo.db.ClimberInfo.find_one({"username": username})

    if climber_info is not None:
        climber_info_object = load_climber_info_object(climber_info)
        routes = load_routes(username)

        return Climber(username, info=climber_info_object, routes=routes)

class LoginController(View):
    """ Renders a login view and gives the view a login form. If the controller
        recieves a POST request it validates the form and on success logins the user.
    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    methods = ["GET", "POST"]

    def dispatch_request(self):
        """ Renders the Login HTML page.
        Parameters
        ----------
        None

        Returns
        -------
        template (View): Rendered HTML page.
        """
        form = LoginSignupForm()

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            found_climber = mongo.db.Climbers.find_one(
                {"username": username, "password": password})

            if found_climber is not None:
                login_user(load_climber(found_climber["username"]))
                return redirect('climberRoutes')

            flash("Either the user doesn't exist or the password was incorrect.")
        return render_template('login.html', form=form)

class LogoutController(View):
    """ Renders a logout view. Uses the Flask Login library to logout the user. If the controller
        recieves a POST request it validates the form and on success logouts the user.
    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    methods = ["GET", "POST"]

    def dispatch_request(self):
        """ Renders the Logout HTML page.
        Parameters
        ----------
        None

        Returns
        -------
        template (View): Rendered HTML page.
        """
        logout_user()
        flash('You are now logged out.', 'success')
        return redirect('login')

class SignupController(View):
    """ Renders signup view. If the controller recieves a POST request it 
        validates the form and on success signs a user up.
    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    methods = ["GET", "POST"]

    def dispatch_request(self):
        """ Renders the Signup HTML page. Displays base page on GET request and on POST
            request signs up a user.
        Parameters
        ----------
        None

        Returns
        -------
        template (View): Rendered HTML page.
        """
        form = LoginSignupForm()

        if form.validate_on_submit():
            if self.update_database(form):
                return render_template("login.html", form=form)

            flash('That username already exists!')
        return render_template('signup.html', form=form)

    def update_database(self, form):
        """ Takes a valid form and updates the Mongo DB with the newly created user.
        Parameters
        ----------
        form (dict): Form submitted from POST request.

        Returns
        -------
        success (Bool): Returns True if update was a success, else error.
        """
        username = form.username.data
        password = form.password.data

        existing_user = mongo.db.Climbers.find_one({"username": username})

        if existing_user is None:
            mongo.db.Climbers.insert(
                {'username': username, 'password': password})

            info_attributes = ['firstname', 'lastname', "street", "city",
                               "state", "zip_code", 'phone_number', 'favoriteGym']

            # Every climber starts with a beginner skill value until they change it manually.
            climber_info_dict = {'username': username,
                                 "climbingLevel": SkillLevel.beginner.value}
            # Creates empty fields for a climber. They must update these fields manually in the app.
            for attribte in info_attributes:
                climber_info_dict[attribte] = ""

            mongo.db.ClimberInfo.insert(climber_info_dict)

            return True

class ClimberInfoController(View):
    """ Renders the ClimberInfo view. If the controller recieves a POST request 
        it validates the form and on success updates the Climber object and database.
    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    methods = ["GET", "POST"]
    decorators = [login_required]

    def dispatch_request(self):
        """ Renders the ClimberInfo HTML page. Displays base page on GET request and on POST
            request updates a Climber's ClimberInfo object and the Mongo DB.
        Parameters
        ----------
        None

        Returns
        -------
        template (View): Rendered HTML page.
        """
        form = ClimberInfoForm()

        if form.validate_on_submit():
            if self.update_database(form):
                flash("Succesfully updated info.")
                form = ClimberInfoForm()

                return redirect(url_for('climberInfo', form=form))

            flash("Error when updating info.")
        return render_template('climberInfo.html', form=form)

    def update_database(self, form):
        """ Takes a valid form and updates the Mongo DB with the climber's
            updated personal info.
        Parameters
        ----------
        form (dict): Form submitted from POST request.

        Returns
        -------
        success (Bool): Returns True if update was a success, else error.
        """
        climber_info = mongo.db.ClimberInfo
        for element in form:
            if len(element.data) > 0:
                climber_info.update({"username": current_user.get_username()}, {
                                    "$set": {element.id: element.data}})
        return True

class ClimberRouteController(View):
    """ Renders the ClimberRoute view. If the controller recieves a POST 
        request it validates the form and on success creates a new route 
        and adds it to the Climber object and database.
    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    methods = ["GET", "POST"]
    decorators = [login_required]

    def dispatch_request(self):
        """ Renders the ClimberRoute HTML page. Displays base page on GET request and on POST
            request updates a Climber's Route object and the Mongo DB.
        Parameters
        ----------
        None

        Returns
        -------
        template (View): Rendered HTML page.
        """
        form = ClimberRouteForm()
        
        if len(list(request.form)) > 0 and "Delete" in list(request.form)[0]:
            self.delete_route(list(request.form)[0])
            return redirect(url_for('climberRoutes', form=form, ))

        if form.validate_on_submit():
            if self.update_database(form):

                flash("Successfully added route.")
                return redirect(url_for('climberRoutes', form=form, ))

            flash("Route Name is taken already.")
            form = ClimberRouteForm()

        return render_template('climberRoutes.html', form=form)

    def delete_route(self, route):
        """ Takes a valid delete request, parses the route name and removes the route of the database.
        Parameters
        ----------
        route (str): The route with its delete member.

        Returns
        -------
        None
        """
        route = route.split(",")[1].replace(")","").replace("\"","").replace("'","").replace(" ","")
        mongo.db.Routes.remove({"route_name":str(route)})

    def update_database(self, form):
        """ Takes a valid form and updates the Mongo DB with the climber's
            updated route info.
        Parameters
        ----------
        form (dict): Form submitted from POST request.

        Returns
        -------
        success (Bool): Returns True if update was a success, else error.
        """
        if not mongo.db.Routes.find_one({"route_name": form.route_name.data}):
            routes_dict = {"username": current_user.get_username()}

            for element in form:
                routes_dict[element.id] = element.data

            mongo.db.Routes.insert(routes_dict)
            return True

        return False

class WorkoutGeneratorController(View):
    """ Renders the WorkoutGenerator view. If the controller recieves a POST 
        request it validates the form and on success renders the WorkoutGenerator
        view with a workout object passed into the view to be displayed.
    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    methods = ["GET", "POST"]
    decorators = [login_required]

    def dispatch_request(self):
        """ Renders the WorkoutGenerator HTML page. Displays base page on GET request and on POST
            request displays a Workout object to HTML.
        Parameters
        ----------
        None

        Returns
        -------
        template (View): Rendered HTML page.
        """
        form = WorkoutForm()

        if form.validate_on_submit():
            routes = list(mongo.db.Routes.find({"location": form.gym.data}))
            workout = Workout(routes, form, self.determine_workout_strategy())
            return render_template('generateWorkout.html', form=form, workout=workout)

        return render_template('generateWorkout.html', form=form, )

    def determine_workout_strategy(self):
        """ Makes use of the strategy design pattern and uses the Climber's personal
            skill level to determine the algorithm to select for generating a workout.
        Parameters
        ----------
        None

        Returns
        -------
        workout_algorithm (WorkoutStrategy): Workout algorithm to be used to generate a workout.
        """
        if current_user.get_info().get_skill_level() == SkillLevel.beginner.value:
            return BeginnerWorkout()
        elif current_user.get_info().get_skill_level() == SkillLevel.intermediate.value:
            return IntermediateWorkout()
        elif current_user.get_info().get_skill_level() == SkillLevel.advanced.value:
            return AdvancedWorkout()

app.add_url_rule('/login', view_func=LoginController.as_view('login'))
app.add_url_rule('/logout', view_func=LogoutController.as_view('logout'))
app.add_url_rule('/signup', view_func=SignupController.as_view('signup'))
app.add_url_rule('/climberInfo', view_func=ClimberInfoController.as_view('climberInfo'))
app.add_url_rule('/climberRoutes', view_func=ClimberRouteController.as_view('climberRoutes'))
app.add_url_rule('/generateWorkout', view_func=WorkoutGeneratorController.as_view('generateWorkout'))

if __name__ == '__main__':
    app.run(debug=True)
