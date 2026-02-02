from flask import Flask, render_template, request, flash, redirect, url_for, session
from models import db, User
from datetime import datetime
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = "secret_key" #Flask messages require a secret key

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rolsa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='avery_long_secret_random_key'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def homepage():
    return render_template('homepage.html')

#This leads users to the Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == "POST":

        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email").strip()
        plain_password = request.form.get('password').strip()
        dob = request.form.get("dob").strip()
        gender = request.form.get("gender")

    # Validations for Registration forms
        existing_user = User.query.filter((User.fullname == fullname) | (User.email == email)).first()
        if existing_user:
            if existing_user.fullname == fullname:
                return render_template("register.html", message="Username already exists", message_type="error")
        
            elif existing_user.email == email:
                return render_template("register.html", message="Email already registered", message_type="error")
            
        if not fullname or not email or not plain_password or not dob or not gender: 
            return render_template("register.html", message="All fields are required", message_type="error")
        
        if not "@" in email and "." not in email: 
            return render_template("register.html", message="Invalid email format", message_type="error")
        
        if len(plain_password) < 8 or len(plain_password) > 20:
            return render_template('register.html', message="Password must be between 8 and 20 characters long", message_type="error")

        try:
            dob = datetime.strptime(dob, '%Y-%m-%d').date()
        except ValueError:
            return render_template('register.html', message="Invalid date format. Use YYYY-MM-DD", message_type="error")

    # Gender validation
        if gender not in ["Male", "Female", "Other"]:
            return render_template('register.html', message="Invalid gender selection", message_type="error")
    
        hashed_password = bcrypt.generate_password_hash(plain_password).decode('utf-8')

     #save to database 
        try: 
            save_user = User(fullname=fullname, email=email, password=hashed_password, dob=dob, gender=gender)
            db.session.add(save_user)
            db.session.commit()
            return render_template('login.html', message="Registration successful!", message_type="success")
        except Exception as e:
            return render_template("register.html", message=f"An error occurred: {e}", message_type="error")
        
    return render_template('register.html')

#This leads users to the Login Page
@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email')
        plain_password =  request.form.get('password').strip()

        user = User.query.filter_by(email = email).first()

    #Validations for the Login Form
        if user and bcrypt.check_password_hash(user.password, plain_password):   
            #This stores users info in session
            session['user_id'] = user.id
            session['user_email'] = user.email

            return render_template('articles.html', message="You've been logged in successfuly!", message_type="success")
            
        if not email or not plain_password:
             return render_template("login.html", message="All fields are required", message_type="error")

        else:
            return render_template('login.html', message="Login Failed, Please check your Email Address and Password and Try Again",  message_type="error")
        
    return render_template('login.html')
 
@app.route('/carbon_footprint.html')
def carbon_footprint():
    return render_template('carbon_footprint.html')

@app.route('/energy_usage.html')
def energy_usage():
    return render_template('energy_usage.html')

@app.route('/schedule.html')
def schedule():
    return render_template('schedule.html')


@app.route('/articles.html')
def articles():


    # To ensure users have been logged in to access the articles page. 
    if 'user_id' not in session:
        return render_template('articles.html', message="Please ensure you've been logged in to view this content!", message_type="error")

    return render_template('articles.html')



@app.route('/admin')
def admin():
   return render_template('admin')


#This helps in running the app in debug mode. By reloading the server when code changes.
if __name__ == '__main__':
    app.run(debug=True)