import bcrypt
from flask import Flask, render_template, request, session, redirect
from pymongo import MongoClient
app = Flask(__name__)

app.secret_key = "TriadAINSTL"

client = MongoClient(
    "mongodb+srv://pandeysheril12469_db_user:Zd3JHLqyGEQoGbgz@userdb.4tviahr.mongodb.net/?appName=UserDB"
)


db = client["userDB"]
users = db["users"]

@app.route("/login")
def home():
    return render_template("login.html")


@app.route('/')
def index():
    return render_template('index.html')

## REGISTER ROUTE
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            return "Passwords do not match"

        existing = users.find_one({
            "$or": [
                {"email": email},
                {"phone": phone}
            ]
        })

        if existing:
            return "User already exists"

        hashed = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )

        users.insert_one({
            "name": name,
            "email": email,
            "phone": phone,
            "password": hashed
        })

        return redirect('/login')

    return render_template('register.html')

## LOGIN ROUTE
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        identifier = request.form['identifier']
        password = request.form['password']

        user = users.find_one({
            "$or": [
                {"email": identifier},
                {"phone": identifier}
            ]
        })

        if user:

            if bcrypt.checkpw(
                password.encode('utf-8'),
                user['password']
            ):

                session['user'] = str(user['_id'])
                session['name'] = user['name']

                return redirect('/dashboard')

        return "Invalid credentials"

    return render_template('login.html')

##Dashboard route
@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    return render_template(
        'dashboard.html',
        name=session['name']
    )

##Logout route
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

##Forgot password route
@app.route('/forgot-password',
           methods=['GET', 'POST'])
def forgot_password():

    if request.method == 'POST':

        email = request.form['email']
        new_password = request.form['password']

        hashed = bcrypt.hashpw(
            new_password.encode('utf-8'),
            bcrypt.gensalt()
        )

        users.update_one(
            {"email": email},
            {"$set": {"password": hashed}}
        )

        return redirect('/login')

    return render_template(
        'forgot_password.html'
    )

if __name__ == '__main__':
    app.run(debug=True)