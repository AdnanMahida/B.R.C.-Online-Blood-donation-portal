from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '********'

# Enter your database connection details below
app.config['MYSQL_HOST'] = '********'
app.config['MYSQL_USER'] = '********'
app.config['MYSQL_PASSWORD'] = '********'
app.config['MYSQL_DB'] = '********'

# Intialize MySQL
mysql = MySQL(app)
#templates rendering
@app.route('/')
def index():
    request_list_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    blood_group_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    blood_stock_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_list_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    blood_group_cursor.execute("SELECT * FROM blood_group")
    blood_group=blood_group_cursor.fetchall()

    request_list_cursor.execute("SELECT * FROM blood_request_list")
    request_list = request_list_cursor.fetchall()
    
    blood_stock_cursor.execute("SELECT * FROM blood_stock,blood_group where blood_stock.blood_stock_id = blood_group.blood_group_id")
    blood_stock=blood_stock_cursor.fetchall()

    if "loggedin" in session:
        user_id = session['id']
        request_list_query = """
                SELECT 
                    blood_request.blood_request_id AS blood_request_id,
                    blood_group.blood_group_id AS blood_group_id,
                    blood_group.blood_group_name AS blood_group_name,
                    users.full_name AS full_name,
                    users.city AS city,
                    users.contact AS contact,
                    blood_request.blood_qty_ml AS blood_qty_ml,
                    blood_request.is_approved AS is_approved,
                    blood_request.timestamp AS timestamp
                FROM
                    ((blood_group
                    JOIN blood_request)
                    JOIN users)
                WHERE
                    ((blood_request.blood_group_id = blood_group.blood_group_id)
                    AND (blood_request.user_id = users.user_id))
                    AND users.user_id <> %s
                ORDER BY blood_request.blood_request_id
        """

        request_list_cursor.execute(request_list_query,[user_id])
        request_list = request_list_cursor.fetchall()

        query="""
                SELECT 
                    blood_request.blood_request_id AS blood_request_id,
                    blood_group.blood_group_id AS blood_group_id,
                    blood_group.blood_group_name AS blood_group_name,
                    users.full_name AS full_name,
                    users.city AS city,
                    users.contact AS contact,
                    blood_request.blood_qty_ml AS blood_qty_ml,
                    blood_request.is_approved AS is_approved,
                    blood_request.timestamp AS timestamp
                FROM
                    ((blood_group
                    JOIN blood_request)
                    JOIN users)
                WHERE
                    ((blood_request.blood_group_id = blood_group.blood_group_id)
                        AND (blood_request.user_id = users.user_id))
                        AND users.user_id = %s
                ORDER BY blood_request.blood_request_id
            """
        
        my_list_cursor.execute(query,[user_id])
        my_request_list=my_list_cursor.fetchall()
        return render_template('index.html',my_request_list = my_request_list,request_list=request_list,blood_group=blood_group,blood_stock=blood_stock)
    return render_template('index.html',blood_stock=blood_stock,request_list=request_list)
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
        email = request.form['email']
        password = request.form['password']

        print('Login successful')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()

        if user:
            session['loggedin'] = True
            session['id'] = user['user_id']
            session['email'] = user['email']
            return redirect(url_for('index'))
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
    return render_template('signup.html', title="Register",blood_group=blood_group)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/info-user',methods=['GET', 'POST'])
def info_user():
    flash("for your interest in blood donation, We have sent address & other details through registered mail and contact number, you can also visit our B.R.C. hospital for more information", "success")
    return redirect(url_for('index'))


@app.route('/insert-donation',methods=['GET', 'POST'])
def insert_dontation():
    if request.method == 'POST' and 'fullname' in request.form:
        blood_group  = request.form['blood_group_id']
        blood_qty  = request.form['blood_qty']
        user_id = session['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query ='INSERT INTO blood_request VALUES (NULL,%s,%s,%s,0,NULL,CURRENT_TIMESTAMP)'
        t  = (user_id, blood_group, blood_qty,)
        cursor.execute(query,t)
        mysql.connection.commit()
        flash("You have successfully applied!", "success")
    return redirect(url_for('index'))

@app.route('/update-request/<int:id>',methods=['GET', 'POST'])
def update_request(id):
    if request.view_args['id']:
        user_id = session['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query ='UPDATE blood_request SET is_approved = 1, donor_id = %s WHERE blood_request_id = %s'
        t  = (user_id,id)
        cursor.execute(query,t)
        mysql.connection.commit()
        flash("for your interest in blood donation, We have sent address & other details through registered mail and contact number, you can also visit our B.R.C. hospital for more information", "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()