"""
TEMPLATE - Use template to define how to generate a workout
UNDO/MOMENTO - UNDO ROUTES
FACTORY - Use a factory to generate routes.

"""
from flask import Flask, render_template, flash, request, abort, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, DecimalField, SelectMultipleField
from flask_pymongo import PyMongo 
from flask_wtf import FlaskForm
from flask.views import View

# Class Imports
from classes.ClimberInfo import ClimberInfo
from classes.Climber import Climber
from classes.RouteFactory import RouteFactory, BoulderingTypes

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config["MONGO_URI"] = "mongodb://localhost/Flash"
mongo = PyMongo(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_climber(username):
    climber_info = mongo.db.ClimberInfo.find_one({"username":username})
    if climber_info is not None:

        firstname = climber_info["firstname"]
        lastname = climber_info["lastname"]
        address = climber_info["address"]
        phone_number = climber_info["phoneNumber"]
        favoriteGym = climber_info["favoriteGym"] 

        climber_info_object = ClimberInfo(firstname, lastname, address, phone_number)
        ############################################################################
        routes = mongo.db.Routes.find({"username":username})
        created_routes = []
        for route in routes:
            created_route = RouteFactory.createRoute(RouteFactory(),route["routeType"], route["routeName"], route["location"], 
            route["holds"],route["actualDifficulty"],route["feltDifficulty"])
            created_routes.append(created_route)
        print(created_routes)
        ############################################################################
        climbers = mongo.db.Climbers.find_one({"username":username})
        username = username
        password = climbers["password"]      
        
        return Climber(username, password, info=climber_info_object, favoriteGym=favoriteGym, routes=created_routes)

class LoginSignupForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=3, max=25), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class ClimberInfoForm(FlaskForm):
    firstname = StringField('Firstname')
    lastname = StringField('Lastname')
    address = StringField('Address')
    phoneNumber = StringField('PhoneNumber')
    favoriteGym = StringField('FavoriteGym')

class ClimberRouteForm(FlaskForm):
    holdTypes = ["Crimpy", "Jugs", "Edges", "Pinch", "Sloper", "Pocket", "Undercling", "Flake", "Horn"]
    holdTypes = [(hold, hold) for hold in holdTypes]

    routeTypes = ["Boulder", "Lead", "TopRope"]
    routeTypes = [(routeType, routeType) for routeType in routeTypes]

    routeName = StringField('RouteName', [validators.DataRequired()])
    routeType = SelectField('RouteType', [validators.DataRequired()], choices=routeTypes)

    location = StringField('Location', [validators.DataRequired()])
    holds = SelectMultipleField('Holds', [validators.DataRequired()], choices=holdTypes)

    actualDifficulty = StringField('ActualDifficulty', [validators.DataRequired()])
    feltDifficulty = StringField('FeltDifficulty', [validators.DataRequired()])

class LoginController(View):
    methods = ["GET", "POST"]

    def dispatch_request(self):
        form = LoginSignupForm()

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            
            climbers =  mongo.db.Climbers
            found_climber = climbers.find_one({"username":username, "password":password})

            if found_climber is not None:
                login_user(load_climber(found_climber["username"]))
                return render_template('index.html')

            flash("Either the user doesn't exist or the password was incorrect.")
            return render_template('login.html', form=form)

        return render_template('login.html', form=form)   
    
class LogoutController(View):
    methods = ["GET", "POST"]

    def dispatch_request(self):
        logout_user()
        form = LoginSignupForm()
        flash('You are now logged out.', 'success')
        return render_template('login.html', form=form)

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
        
        climbers = mongo.db.Climbers
        existing_user = climbers.find_one({"username":username})

        if existing_user is None:
            climbers.insert({'username': username, 'password' : password})
            info_attributes = ['firstname', 'lastname', 'address', 'phoneNumber', 'favoriteGym']
            
            climber_info_dict = {'username':username}
            for attribte in info_attributes: climber_info_dict[attribte] = ""
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
                climber_info.update({"username":current_user.getUsername()}, {"$set": {element.id:element.data}})
        
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
        if not mongo.db.Routes.find_one({"routeName":form.routeName.data}):
            routes_dict = {"username": current_user.getUsername()}

            for element in form: routes_dict[element.id] = element.data
            print('SHSHDHSDHSHDHS')
            print(routes_dict)
            mongo.db.Routes.insert(routes_dict)

            success = True
        
        return success


app.add_url_rule('/login', view_func=LoginController.as_view('login'))
app.add_url_rule('/logout', view_func=LogoutController.as_view('logout'))
app.add_url_rule('/signup', view_func=SignupController.as_view('signup'))
app.add_url_rule('/climberInfo', view_func=ClimberInfoController.as_view('climberInfo'))
app.add_url_rule('/climberRoutes', view_func=ClimberRouteController.as_view('climberRoutes'))



@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/generateWorkout')
@login_required
def generateWorkout():
    return render_template('generateWorkout.html')

if __name__ == '__main__':
    app.run(debug=True)

