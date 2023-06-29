from flask import Flask, render_template, request, session, redirect, url_for
import os
import hashlib
from datetime import datetime
from query import runQuery

app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def validate(email):
    userId = None
    result = runQuery("SELECT userid FROM users WHERE email = '" + email + "'","select")
    if result:
        userId = result[0]["userid"]
    return userId

def is_valid(email, password):
    data = runQuery("SELECT email, password, usertype FROM users WHERE email='{}' and password='{}'".format(email,hashlib.md5(password.encode()).hexdigest()),"select")
    if data:
        return (True,data[0])
    return (False,{})

def makeSignin():
    if 'email' not in session:
        loggedIn = False
        userData = {}
    else:
        loggedIn = True
        userData = {}
        userData = runQuery("SELECT * FROM users WHERE email = '" + session['email'] + "'","select")
        if len(userData)>0:
            userData = userData[0]
    return (userData, loggedIn)

@app.route("/dashboard")
def dashboard():
    if 'email' not in session:
        return redirect(url_for('root'))
    userData, loggedIn = makeSignin()
    itemData = runQuery('SELECT * FROM bikes where status = 1'.format(userData["userid"]),"select")

    return render_template("dashboard.html", userData=userData, itemData=itemData, loggedIn=loggedIn)

@app.route("/addBike", methods=["GET", "POST"])
def addBike():
    if 'email' not in session:
        return redirect(url_for('root'))

    userData, loggedIn = makeSignin()

    if request.method == 'GET':
        return render_template("add_bike.html",userData=userData , loggedIn=loggedIn)
    elif request.method == 'POST':
        file1 = request.files["image"]
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        image = file1.filename

        file1.save(path)

        bikeName = request.form['bikeName']
        description = request.form['description']
        engine = request.form['engine']
        mileage = request.form['mileage']
        transmission = request.form['transmission']
        price = request.form['price']
        createdate = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
        updatedate = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")

        try:
            result = runQuery("INSERT INTO bikes (userid,image,bikeName,description,engine,mileage,transmission,price,createdate,updatedate) VALUES ({},'{}','{}','{}','{}','{}','{}','{}', '{}', '{}')".format(userData["userid"],image,bikeName,description,engine,mileage,transmission,price,createdate,updatedate),"insert")
            response = "Request is completed successfully."
            return redirect(url_for('dashboard'))
        except Exception as e:
            print(e)
            response = "Request is failed."
            return render_template("addBook.html",error=response)

@app.route("/")
def root():
    userData, loggedIn = makeSignin()
    itemData = runQuery('SELECT * FROM bikes where status = 1 limit 2'.format(userData["userid"]),"select")
    return render_template("index.html", userData = userData, loggedIn=loggedIn, itemData=itemData)

@app.route("/bike_listing")
def bike_listing():
    userData, loggedIn = makeSignin()
    itemData = runQuery('SELECT * FROM bikes where status = 1'.format(userData["userid"]),"select")
    return render_template("bike_listing.html", userData = userData, loggedIn=loggedIn, itemData=itemData)

@app.route("/bike_detail")
def bike_detail():
    userData, loggedIn = makeSignin()
    itemData = runQuery('SELECT * FROM bikes where status = 1'.format(userData["userid"]),"select")
    return render_template("bike_detail.html", userData = userData, loggedIn=loggedIn, itemData=itemData)

@app.route("/gallery")
def gallery():
    userData, loggedIn = makeSignin()
    return render_template("gallery.html", userData = userData, loggedIn=loggedIn)

@app.route("/about")
def about():
    userData, loggedIn = makeSignin()
    return render_template("about.html", userData = userData, loggedIn=loggedIn)

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        if 'email' in session:
            return redirect(url_for('root'))
        else:
            return render_template('login.html', error='')
    elif request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        status,data = is_valid(email, password)
        if status:
            session['email'] = email
            if data["usertype"] == "author":
                return redirect(url_for('bike_listing'))
            else:
                return redirect(url_for('root'))
        else:
            error = 'Invalid Email or Password. Please try again.'
            return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('root'))

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            return render_template("register.html", error="Password did not match!") 
        email = request.form['email'].strip().lower()
        first_name = request.form['first_name']
        last_name = request.form['first_name']
        age = int(request.form['age'])
        address = request.form['address']
        userType = "user"
        print(password, email, first_name, last_name, age, address)
        createDate = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")

        if (validate(email)) != None:
            return render_template("login.html", error="Email already exist.")
        else:
            try:
                runQuery("INSERT INTO users (password, email, first_name, last_name, age, address, userType, createDate) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(hashlib.md5(password.encode()).hexdigest(), email, first_name, last_name, age, address, userType, createDate),"insert")
                response = "Request is completed successfully."
                
            except Exception as e:
                print(e)
                response = "Request is failed."
            print(response)
            return render_template("login.html", error=response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)