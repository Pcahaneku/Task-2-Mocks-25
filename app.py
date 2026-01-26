from flask import Flask, render_template, request, flash, redirect, url_for
from models import db, User
from datetime import datetime
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "a_very_secret_random_string"

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
@app.route('/register') 
def register():
    return render_template('register.html') 

@app.route('/register', methods=['POST'])
def add_users():

    if request.method == "POST":

        fullname = request.form.get("fullname").strip()
        email = request.form.get("email").strip()
        plain_password = request.form.get('password').strip()
        hashed_password = bcrypt.generate_password_hash(plain_password).decode('utf-8')
        dob = request.form.get("dob").strip()
        gender = request.form.get("gender")

#validation
    if not fullname or not email or not plain_password or not dob or not gender:
        flash('All fields are required!')
        return redirect(url_for("register"))
    
    elif len(plain_password) > 8:
        flash('Password must be up to 8 characters')
        return redirect(url_for("register"))
    
    elif len(plain_password) <= 7:
        flash('Password must be at least 8.')
        return redirect(url_for("register"))

    elif dob:
        try:
            dob = datetime.strptime(dob, '%Y-%m-%d').date() #Converts the date of birth string to a date object
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD."

    elif gender not in ["Male", "Female", "Other"]:
        flash('Invalid gender selection')
        return redirect(url_for("register"))
    
    else:
        flash('User Registered Successfully!')
        return redirect(url_for('login'))
    
     #save to database 
    save_user = User(fullname=fullname, email=email, password=hashed_password, dob=dob, gender=gender)

    try: 
        db.session.add(save_user)
        db.session.commit()
        return render_template('/login.html')
    except Exception as e:
        return f"An error occured: {e}"

@app.route('/login')
def login():
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


@app.route('/information.html')
def info():
    return render_template('information.html')

@app.route('/admin')
def admin():
   return render_template('admin')


#This helps in running the app in debug mode. By reloading the server when code changes.
if __name__ == '__main__':
    app.run(debug=True)