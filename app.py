from flask import Flask, render_template, request, redirect, session
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = "royalindia123"

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@123",
    database="royal_india_travels"
)
if not db.is_connected():
    db.reconnect()
cur = db.cursor()

# ---------------- HOME ----------------
@app.route('/')
def home():
    cur = db.cursor()
    cur.execute("SELECT * FROM packages")
    packages = cur.fetchall()
    cur.close()
    return render_template('index.html', packages=packages)

# ---------------- ABOUT ----------------
@app.route('/about')
def about():
    return render_template('about.html')

# ---------------- CONTACT ----------------
@app.route('/contact')
def contact():
    return render_template('contact.html')

# ---------------- PACKAGE DETAILS ----------------
@app.route('/package/<name>')
def package_details(name):
    return render_template('package_details.html', package=name)

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cur = db.cursor()
        cur.execute(
            "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
            (name, email, password)
        )
        db.commit()
        cur.close()

        return redirect('/login')

    return render_template('register.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = db.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cur.fetchone()
        cur.close()

        if user:
            session['user'] = user[1]
            session['user_email'] = user[2]
            return redirect('/dashboard')
        else:
            return "Invalid Login"

    return render_template('login.html')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ---------------- BOOKING ----------------
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        location = request.form['location']
        package_name = request.form['package_name']
        persons = request.form['persons']
        travel_date = request.form['travel_date']

        cur = db.cursor()
        cur.execute("""
        INSERT INTO bookings
        (fullname,email,location,package_name,persons,travel_date,entry_date,entry_time)
        VALUES(%s,%s,%s,%s,%s,%s,CURDATE(),CURTIME())
        """, (fullname,email,location,package_name,persons,travel_date))

        db.commit()
        cur.close()

        return redirect('/payment')

    return render_template('booking.html')

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    return render_template('payment.html')

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    return "Payment Successful! Booking Confirmed"

@app.route('/invoice')
def invoice():
    return render_template('invoice.html')

# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        return redirect('/login')

    email = session['user_email']

    cur = db.cursor()
    cur.execute("SELECT * FROM bookings WHERE email=%s", (email,))
    bookings = cur.fetchall()
    cur.close()

    return render_template(
        'dashboard.html',
        username=session['user'],
        bookings=bookings
    )

# ---------------- ADMIN ----------------
@app.route('/admin')
def admin():

    if 'admin' not in session:
        return redirect('/admin_login')

    cur = db.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    cur.execute("SELECT * FROM bookings")
    bookings = cur.fetchall()

    cur.execute("SELECT * FROM packages")
    packages = cur.fetchall()

    cur.close()

    return render_template(
        'admin.html',
        users=users,
        bookings=bookings,
        packages=packages
    )

@app.route('/add_package', methods=['GET', 'POST'])
def add_package():

    if request.method == 'POST':
        name = request.form['name']
        image = request.form['image']
        days = request.form['days']
        price = request.form['price']
        category = request.form['category']

        cur = db.cursor()
        cur.execute("""
            INSERT INTO packages(name,image,days,price,category)
            VALUES(%s,%s,%s,%s,%s)
        """, (name,image,days,price,category))

        db.commit()
        cur.close()

        return redirect('/admin')

    return render_template('add_package.html')

@app.route('/delete_package/<int:id>')
def delete_package(id):

    cur = db.cursor()
    cur.execute("DELETE FROM packages WHERE id=%s", (id,))
    db.commit()
    cur.close()

    return redirect('/admin')


@app.route('/delete_booking/<int:id>')
def delete_booking(id):

    cur = db.cursor()
    cur.execute("DELETE FROM bookings WHERE id=%s", (id,))
    db.commit()
    cur.close()

    return redirect('/admin')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect('/admin')
        else:
            return "Invalid Admin Login"

    return render_template('admin_login.html')

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin', None)
    return redirect('/admin_login')


@app.route('/packages')
def packages():
    return render_template('packages.html')


@app.route('/goa')
def goa():
    return render_template("goa.html")

@app.route('/kashmir')
def kashmir():
    return render_template("kashmir.html")

@app.route('/ladakh')
def ladakh():
    return render_template("ladakh.html")

@app.route('/kerala')
def kerala():
    return render_template("kerala.html")

@app.route('/manali')
def manali():
    return render_template("manali.html")

@app.route('/jaipur')
def jaipur():
    return render_template("jaipur.html")


@app.route('/details/<place>')
def details(place):
    return render_template("details.html", place=place.lower())


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)