
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helper import login_required,cardCheck,error_message

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///hotel.db")



# Card check for account crediting for services

@app.route("/services" , methods=["POST"])
@login_required
def dashboard2():

    # if request.method == "POST":
    card = request.form.get("credit_num")
    laundry = request.form.get("option1")
    swimming = request.form.get("option2")
    food = request.form.get("option3")
    gyming = request.form.get("option4")
    massage = request.form.get("option5")


    list_details = [laundry,swimming,food,gyming,massage]
    # print(list_details)

    services = {
        "laundry" : 100,
        "swimming" : 200,
        "food" : 300,
        "gyming" : 400,
        "massage" : 500
    }

    if cardCheck(card):
        for i,service in zip(range(len(services)),services):

            if list_details[i] == None:
                services[service] = 0
            else:
                services[service] = services[service]
        # print(services)
        expenses = sum([services[service] for service in services])
        db.execute("INSERT INTO services(laundry, swimming, food, gyming, massage, user_id, expenses) VALUES (?,?,?,?,?,?,?)",services["laundry"],services["swimming"],services["food"],services["gyming"],services["massage"],session["user_id"],expenses)
        flash("Payment Successful!")
        return redirect("/dashboard")

    else:

        return error_message("Invalid Card",400)

        # return

# Card check for account crediting for rooms/booking
@app.route("/booking" , methods=["POST","GET"])
@login_required
def dashboard():

    if request.method == "POST":
        card = request.form["cardnumber"]

        option = request.form["exampleRadios"]
        duration = int(request.form["duration"])
        rooms = {
            "Violet" : 1000,
            "Magenta" : 2000,
            "Indigo" : 3000
        }

        total = duration * rooms[option]

        if cardCheck(card):

            db.execute("INSERT INTO bookings(room_type, duration, price,total, user_id) VALUES (?,?,?,?,?)",
            option,duration,rooms[option],total,session["user_id"])
            flash("Payment Successful!")

        else:

            return error_message("Invalid Card",400)

        return redirect("/dashboard")



# Front page
@app.route("/")
def index():
    """Show front page at first visit  """
    return render_template("homepage.html")




# Login session
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error_message("Username must be provided!",400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error_message("Password cannot be empty!",400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return error_message("Invalid username and/or password",400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]


        for i in range(len(rows)):

            if rows[i]["user_role"] == "admin":
                # Redirect user to home page
                return redirect("/admin")
            else:
                flash("Login Successful")
                return redirect("/dashboard")
        # return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# Logout session
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# Redistration session
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        role = "user"
        username = request.form.get("username").lower()
        f_name = request.form.get("f_name").lower()
        l_name = request.form.get("l_name").lower()
        p_number = request.form.get("p_number")
        password = request.form.get("password")
        password1 = request.form.get("confirmation")
        data = db.execute("SELECT COUNT(username) FROM users WHERE username = ?",username)

        if ((not username) or (not f_name) or (not l_name)):
            return error_message("Username/Names fields cannot be empty",400)

        elif ((not p_number) or (p_number.isnumeric()!=True) or len(p_number)< 11):
            return error_message("Phone number not valid",400)

        elif (data[0]["COUNT(username)"] > 0):
            return error_message("Username Already Exist; choose another name!",400)

        elif ((not password) or (not password1)):
            return error_message("Any of the password fields cannot be empty",400)

        elif (password != password1):
            return error_message("Password must be the same!",400)
        name = f_name + l_name
        new_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username,password,name,phone_number,user_role) VALUES (?,?,?,?,?)",username,new_password,name,p_number,role)
        return redirect("/login")
    return render_template("register.html")


# Admin / History Sessions
@app.route("/admin", methods = ["POST","GET"])
@login_required
def admin():
    if db.execute("SELECT user_role FROM users WHERE id = ?", session["user_id"])[0]["user_role"] != "admin":
        return redirect("/dashboard")
    else:
        if request.method == "POST":
            customer = request.form["customer"].lower()
            names = []
            user = db.execute("SELECT username FROM users")
            for name in user:
                names.append(name["username"])
            if customer in names:
                list_services = db.execute("SELECT laundry,swimming,food,gyming,massage,expenses,date FROM services WHERE user_id IN (SELECT id FROM users WHERE username = ?)",customer)

                list_booking = db.execute("SELECT * FROM bookings WHERE user_id IN (SELECT id FROM users WHERE username = ?)",customer)
                # print(list_services)

                values = []
                min_value = []

                for inner in range(len(list_services)):
                    for value in list_services[inner]:
                        if value != "date" and list_services[inner][value] > 0 and value != "expenses":
                            min_value.append(value)

                    values.append(min_value)
                    min_value=[]


                expenses_2 = [str(service[key]) for service in list_services for key in service if key =="date"]
                expenses_1 = [str(serv[keys]) for serv in list_services for keys in serv if keys =="expenses"]
            
                new_values = []
                new_min_value = []
                for ser,exp,dat in zip(values,expenses_1,expenses_2):
                    new_min_value.extend((ser,exp,dat))
                    # print(new_min_value)
                    new_values.append(new_min_value)
                    new_min_value = []



                # print(new_values)
                return render_template("admin.html", booking=list_booking, new_values=new_values)

            else:
                return error_message("User has no record!",400)

        return render_template("admin.html")



# user record tracker

def history():

    list_services = db.execute("SELECT laundry,swimming,food,gyming,massage,expenses,date FROM services WHERE user_id IN (SELECT id FROM users WHERE user_id = ?)",session["user_id"])

    list_booking = db.execute("SELECT * FROM bookings WHERE user_id =?",session["user_id"])
            # print(list_services)

    values = []
    min_value = []

    for inner in range(len(list_services)):
        for value in list_services[inner]:
            if value != "date" and list_services[inner][value] > 0 and value != "expenses":
                min_value.append(value)

        values.append(min_value)
        min_value=[]



    # print(values)

    expenses_2 = [str(service[key]) for service in list_services for key in service if key =="date"]
    expenses_1 = [str(serv[keys]) for serv in list_services for keys in serv if keys =="expenses"]
            # print(expenses_1)
            # print(expenses_2)
    new_values = []
    new_min_value = []
    for ser,exp,dat in zip(values,expenses_1,expenses_2):
        new_min_value.extend((ser,exp,dat))
        new_values.append(new_min_value)
        new_min_value = []

    export = {
                "booking" : list_booking,
                "new_values" : new_values
            }

    return export

# customer page
@app.route("/dashboard")
@login_required
def customer():
    usernam = db.execute("SELECT username,phone_number FROM users WHERE id = ?",session["user_id"])[0]
    username = usernam['username']
    phone_number = usernam['phone_number']

    output = history()
    # print(output)
    return render_template("dashboard.html", output=output, username=username, phone=phone_number)






