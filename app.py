from flask import Flask, render_template, request
from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rolsa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def homepage():
    return render_template('homepage.html')

#Register users
@app.route('/register', methods = ["POST", "GET"])
def register():
    msg = ''
    error = False

    if request.method == ["POST"]:
        full_name = request.form["full_name"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()
        dob = request.form["dob"].strip()
        gender = request.form.getlist["gender"].strip()

    #validation
    if not full_name or not email or not password or not dob or not gender:
        msg = 'All fields are required!'
    elif not is_valid_email(email):
        msg = "Invalid Email Address"
        error = 'True'
    elif len(password) > 8:
        msg = 'Password must be up to 8 characters'
        error = 'True'
    elif len(password) <= 7:
        msg = 'Password must be at least 8.'
        error = 'True'
    else:
        


    return render_template('register.html')



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