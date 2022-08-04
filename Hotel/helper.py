from flask import Flask,session,redirect,render_template
from functools import wraps
from cs50 import SQL
db = SQL("sqlite:///hotel.db")

def login_required(f):
    """
    Decorate routes to require login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def error_message(message,code):
    return render_template("error.html",message=message,code=code)


# Check card function
def cardCheck(card):

    if (card.isnumeric() and ((len(card) >= 13) and (len(card) <= 16))):
                 # last num from the end
        lastDigit = [int(i) for i in card[::-2]]

        # to get the second steps of two from the back
        tweet = card[:-1]
        lastDigitTwo = [int(i) for i in tweet[::-2]]

            # multiple of two of the second numbers
        multipleOfTwo = [(int(i)*2) for i in lastDigitTwo]

            # redefining multiple of two considering number greater tahn 9
        simplifyLastTwo = []
        for i in multipleOfTwo:
            if (len(str(i))) > 1:
                i = str(i)
                j = int(i[0]) + int(i[1])
                simplifyLastTwo.append(j)
            else:
                simplifyLastTwo.append(i)

            # final sum
        finalSum = sum(simplifyLastTwo) + sum(lastDigit)

            # the condiiton test
        test = finalSum % 10
        if test == 0:
            return True
        else:
            return False




# def dashboard2():
#     # value = 10000

#     card = "4003600000000014"
#     laundry = 1
#     swimming = 2
#     food = 3
#     gyming = ""
#     massage = ""

#     list_details = [laundry,swimming,food,gyming,massage]


#     services = {
#             "laundry" : 100,
#             "swimming" : 200,
#             "food" : 300,
#             "gyming" : 400,
#             "massage" : 500
#         }



#     if cardCheck(card):
#         for i,service in zip(range(len(services)),services):

#             if list_details[i] == "":
#                 services[service] = 0
#             else:
#                 services[service] = services[service]
#         print(services)

#         expenses = sum([services[service] for service in services])
#         db.execute("INSERT INTO services(laundry, swimming, food, gyming, massage, user_id, expenses) VALUES (?,?,?,?,?,?,?)",
#         services["laundry"],services["swimming"],services["food"],services["gyming"],services["massage"],1,expenses)


#         print(db.execute("SELECT * FROM services"))
#         print("Payment Successful!")

#     else:
#         # return
#         print("Invalid Card")

# dashboard2()

# def dashboard():
#     username = db.execute("SELECT username,phone_number FROM users WHERE id = ?",1)
#     # username = username[0]['username']
#     phone = username[0]['phone_number']
#     print(username)
#     print(phone)

#     card = "4003600000000014"
#         # deposit = int(request.form["deposit"])
#     option = "room1"
#     duration = int("3")
#     rooms = {
#             "room1" : 1000,
#             "room2" : 2000,
#             "room3" : 3000
#         }

#     total = duration * rooms[option]
#         # value -= rooms[option]


#     if cardCheck(card):
#             # value = deposit
#         db.execute("INSERT INTO bookings(room_type, duration, price,total, user_id) VALUES (?,?,?,?,?)",
#             option,duration,rooms[option],total,1)
#         # print(db.execute("SELECT * FROM bookings"))
#         # print("Payment Successful!")

#     else:
#         print("Invalid Card")

# dashboard()

# def admin():
#     customer = "ope"
#     names = []
#     user = db.execute("SELECT username FROM users")
#     for name in user:
#         names.append(name["username"])
#     if customer in names:
#         list_services = db.execute("SELECT * FROM services WHERE user_id IN (SELECT id FROM users WHERE username = ?)",customer)
#         list_booking = db.execute("SELECT * FROM bookings WHERE user_id IN (SELECT id FROM users WHERE username = ?)",customer)
#         print(f"service: {list_services}")
#         print(f"book: {list_booking}")

#     else:
#         print("User has no record!")
# admin()



# def history():
#     customer = "ope"
#     list_services = db.execute("SELECT laundry,swimming,gyming,food,massage,date,expenses FROM services WHERE user_id IN (SELECT id FROM users WHERE username = ?)",customer)
#     list_booking = db.execute("SELECT room_type,duration,date,total FROM bookings WHERE user_id IN (SELECT id FROM users WHERE username = ?)",customer)

#     # print(list_booking)


#     values = []
#     min_value = []

#     for inner in range(len(list_services)):
#         for value in list_services[inner]:
#             if value != "date" and list_services[inner][value] > 0 and value != "expenses":
#                 min_value.append(value)
#         values.append(min_value)
#         min_value=[]



#     print(values)

#     expenses_1 = [str(service[key]) for service in list_services for key in service if key =="expenses"]
#     expenses_2 = [str(service[key]) for service in list_services for key in service if key =="date"]
#     print(expenses_2)
#     new_values = []
#     new_min_value = []
#     for ser,exp,dat in zip(values,expenses_1,expenses_2):
#         new_min_value.extend((ser,exp,dat))
#         new_values.append(new_min_value)
#         new_min_value = []

# #     # for val in new_values:
# #     #     print(val[0])
# #     #     print(val[1])
# #     #     print(val[2])
# #     # # print((expenses_1))
# #     # # print((expenses_2))
#     print(new_values)


# history()