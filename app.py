from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors
import re

app = Flask(__name__)
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'qwerty123123qwerty'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'brc.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'ad'
app.config['MYSQL_PASSWORD'] = 'bz*J^28<'
app.config['MYSQL_DB'] = 'brc'

# Intialize MySQL
mysql = MySQL(app)
#templates rendering
@app.route('/')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql ="""
    SELECT blood_group.blood_group_id,
    blood_group.blood_group_name,
    users.full_name,
    users.city,
    users.contact,
    blood_request.blood_qty_ml
    FROM blood_group,
    blood_request ,users 
    where blood_request.blood_group_id = blood_group.blood_group_id 
    and blood_request.user_id = users.user_id
    """
    # cursor.execute('SELECT blood_group.blood_group_id,blood_group.blood_group_name,users.full_name,users.city,users.contact,blood_request.blood_qty_mlFROM blood_group,blood_request ,users where blood_request.blood_group_id=blood_group.blood_group_id and blood_request.user_id=users.user_id')
    # cursor.execute(sql)
    cursor.execute("SELECT * FROM blood_request_list")
    request_list = cursor.fetchone()
    print("list of res",request_list)
    
    
    return render_template('index.html',request_list=request_list)

@app.route('/about')
def about():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    return render_template('index.html')

@app.route('/process')
def process():
    return render_template('index.html')

@app.route('/contactus')
def contactus():
    return render_template('index.html')

@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        return render_template('profile.html', username=session['username'], title="Profile")
    return redirect(url_for('login'))

#authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        username = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM users WHERE full_name = %s AND password = %s', (username, password))
        user = cursor.fetchone()

        if user:
            session['loggedin'] = True
            session['id'] = user['user_id']
            session['username'] = user['full_name']
            return redirect(url_for('index'))
        else:
            flash("Incorrect username/password!", "danger")
    return render_template('login.html', title="Login")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'fullname' in request.form:
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']
        contact  = request.form['phone_no']
        blood_group  = request.form['blood_group_id']
        city  = request.form['city']
        is_donor  = 'is_donor' in request.form
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s',[email])
        user = cursor.fetchone()
        if user:
            flash("Account already exists!", "danger")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address!", "danger")
        elif not re.match(r'[A-Za-z0-9]+', email):
            flash("Username must contain only characters and numbers!", "danger")
        elif not email or not password or not email:
            flash("Incorrect username/password!", "danger")
        else:
            
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            query ='INSERT INTO users VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,NULL)'
            t  = (fullname, email, password,contact,city,blood_group,is_donor)
            cursor.execute(query,t)
            mysql.connection.commit()
            flash("You have successfully registered!", "success")
            return redirect(url_for('login'))
    elif request.method == 'POST':
        flash("Please fill out the form!", "danger")
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM blood_group")
    blood_group=cursor.fetchall()
    # print(blood_group)
    return render_template('signup.html', title="Register",blood_group=blood_group)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/user',methods=['GET', 'POST'])
def user():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM user """)
        rows =  cursor.fetchall()
        payload = []
        content = {}
        if mysql:
            return "success"
        # for result in rows:
        #     content = {'username': result[0], 'email': result[1], 'password': result[2]
        #                ,'create_time':result[3]}
        #     payload.append(content)
        #     content = {}
        # return payload
        
    
    except Exception as e:
        return {'error': str(e)}


if __name__ == '__main__':
    app.run(debug=True)