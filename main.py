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

def get_time(comment):
    time = datetime.now()
    # created_date = comment.created_at.astimezone(timezone('Asia/Kolkata'))
    created_date = comment["createdate"]

    start = datetime.strptime(created_date,'%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(datetime.strftime(time,'%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')

    diff_sec = (end -start).total_seconds()

    seconds = diff_sec
    minutes = diff_sec // 60
    hours = (diff_sec // 60) // 60
    days = ((diff_sec // 60) // 60) // 24


    if days > 0:
        return str(int(days)) + " days ago"
    elif hours > 0:
        return str(int(hours)) + " hours ago"
    elif minutes > 0:
        return str(int(minutes)) + " minutes ago"
    elif seconds > 0:
        return str(int(seconds)) + " seconds ago"
    else:
        return "just now"

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
    itemData = runQuery('SELECT * FROM bikes where status = 1',"select")

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
            response = "Request is failed."
            return render_template("addBook.html",error=response)

@app.route("/")
def root():
    userData, loggedIn = makeSignin()
    itemData = runQuery('SELECT * FROM bikes where status = 1 limit 2',"select")
    return render_template("index.html", userData = userData, loggedIn=loggedIn, itemData=itemData)

@app.route("/bike_listing")
def bike_listing():
    userData, loggedIn = makeSignin()
    itemData = runQuery('SELECT * FROM bikes where status = 1',"select")
    return render_template("bike_listing.html", userData = userData, loggedIn=loggedIn, itemData=itemData)

@app.route("/bike_detail/<bike_id>/", methods=["GET", "POST"])
def bike_detail(bike_id):
    userData, loggedIn = makeSignin()
    if request.method == "POST":
        
        if loggedIn:
            comment = request.form['comment']
            ratings = request.form["stars"]
            createDate = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
            try:
                result = runQuery("INSERT INTO comment (userid, bikeid, ratings, message, createdate) VALUES ({}, {}, {}, '{}', '{}')".format(userData["userid"], bike_id, ratings, comment, createDate),"insert")
                response = "Request is completed successfully."
                return redirect(url_for('bike_detail'))
            except:
                response = "Request is failed."
                return redirect(url_for('bike_detail', bike_id=bike_id))
        else:
            return redirect(url_for('bike_detail', bike_id=bike_id))

    itemData = runQuery('SELECT * FROM bikes where bikeId = {} limit 1'.format(bike_id),"select")
    commentsData = runQuery("SELECT cm.commentid,cm.message,cm.createdate,us.first_name from comment as cm left join users as us on us.userid = cm.userid where cm.bikeid = " + bike_id + " ORDER BY cm.commentid","select")
    ratingsData = runQuery("SELECT round(avg(ratings),2) as avg_ratings,count(*) as tot_ratings,count(case ratings when 1 then 1 else null END) as one_rating,count(case ratings when 2 then 1 else null END) as two_rating,count(case ratings when 3 then 1 else null END) as three_rating,count(case ratings when 4 then 1 else null END) as four_rating,count(case ratings when 5 then 1 else null END) as five_rating from comment where bikeid = {}".format(bike_id),"select")
    if len(ratingsData)>0:
        ratingsData = ratingsData[0]

    for comment in commentsData:
        comment["date_diff"] = get_time(comment)
    return render_template("bike_detail.html", userData = userData, commentsData=commentsData,ratingsData=ratingsData, loggedIn=loggedIn, bike=itemData[0])

@app.route("/bikedelete/<bike_id>/", methods=["GET", "POST"])
def deleteBike(bike_id=None):
    if 'email' not in session:
        return redirect(url_for('root'))

    userData, loggedIn = makeSignin()
    if loggedIn and userData["usertype"] == "user":
        return "You are not authorized!"

    if request.method == 'POST':
        try:
            result = runQuery("UPDATE bikes SET status = {} WHERE bikeid = '{}'".format(0,bike_id),"update")
            response = "Request is completed successfully."
            return redirect(url_for('dashboard'))
        except:
            response = "Request is failed."
            return redirect(url_for('dashboard'))

@app.route("/bikedit/<bike_id>/", methods=["GET", "POST"])
def editBook(bike_id=None):
    if 'email' not in session:
        return redirect(url_for('root'))

    userData, loggedIn = makeSignin()

    if loggedIn and userData["usertype"] == "user":
        return "You are not authorized!"

    if request.method == 'GET':
        productData = runQuery("SELECT * FROM bikes WHERE status = 1 and bikeid = " + bike_id +"","select")
        return render_template("editBike.html", userData=userData ,data=productData[0], loggedIn=loggedIn)
    elif request.method == 'POST':
        file1 = request.files["image"]
        if file1:
            path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
            image = file1.filename
            file1.save(path)
        else:
            image = request.form['image']


        bikeName = request.form['bikeName']
        description = request.form['description']
        engine = request.form['engine']
        mileage = request.form['mileage']
        transmission = request.form['transmission']
        price = request.form['price']
        description = request.form['description']
        createdate = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
        updatedate = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")

        try:
            result = runQuery("UPDATE bikes SET userid = {},image = '{}',bikeName = '{}',price = '{}',description = '{}', engine = '{}',mileage = '{}',transmission = '{}',createdate= '{}',updatedate= '{}' WHERE bikeid = '{}'".format(userData["userid"],image,bikeName,price,description,engine,mileage, transmission, createdate,updatedate,bike_id),"update")
            response = "Request is completed successfully."
            return redirect(url_for('dashboard'))
        except:
            response = "Request is failed."
            return render_template("editBike.html",error=response)

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
        userType = request.form['userType']
        createDate = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")

        if (validate(email)) != None:
            return render_template("login.html", error="Email already exist.")
        else:
            try:
                runQuery("INSERT INTO users (password, email, first_name, last_name, age, address, userType, createDate) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(hashlib.md5(password.encode()).hexdigest(), email, first_name, last_name, age, address, userType, createDate),"insert")
                response = "Request is completed successfully."
                
            except Exception as e:
                response = "Request is failed."
            return render_template("login.html", error=response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)