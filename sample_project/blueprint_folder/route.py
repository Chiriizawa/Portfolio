from flask import Flask, Blueprint, redirect, render_template, url_for, session, request, make_response
from werkzeug.security	import generate_password_hash
import mysql.connector

blueprint = Blueprint('blueprint', __name__, template_folder='template')

db_config = {
    'host':'localhost',
    'database':'project_db',
    'user':'root',
    'password':'',
}

def connect_db():
    return mysql.connector.connect(**db_config)

conn = connect_db()
cursor = conn.cursor()

user = {
    'username':'Raymund',
    'password':'123456789'
}

hashed_password = generate_password_hash(user['password'])

def make_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@blueprint.route('/', methods=['POST', 'GET'])
def index():
    if 'user' in session:
        return redirect(url_for('blueprint.dashboard'))

    msg = ''
    if request.method == 'POST':
        Username = request.form['Username']
        Password = request.form['Password']
        if Username == 'Raymund' and Password == '123456789':
            try:
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()
                cursor.execute("INSERT INTO tbl_login (username, password) VALUES(%s, %s)", (user['username'], hashed_password))
                connection.commit()
                session['user'] = Username
                return redirect(url_for('blueprint.dashboard'))
            except mysql.connector.Error as e:
                msg = f"Adding data failed! Error: {str(e)}"
            finally:
                cursor.close()
                connection.close()
        else:
            msg = 'Wrong Credentials!'
    response = make_response(render_template('index.html', msg=msg))
    return make_header(response)

@blueprint.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('blueprint.index'))
    response = make_response(render_template("dashboard.html"))
    response = make_header(response)
    return response

@blueprint.route('/logout')
def logout():
    session.pop('user', None)
    response = make_response(redirect(url_for('blueprint.index')))
    response = make_header(response)

    return response

@blueprint.route('/dashboard/python')
def python():
    if 'user' not in session:
        return redirect(url_for('blueprint.index'))
    response = make_response(render_template('python.html'))
    return make_header(response)

@blueprint.route('/dashboard/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('blueprint.index'))
    response = make_response(render_template('profile.html'))
    return make_header(response)

@blueprint.route('/dashboard/info')
def info():
    if 'user' not in session:
        return redirect(url_for('blueprint.index'))
    
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM tbl_project')
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    response = make_response(render_template('info.html', data=data))
    return make_header(response)

@blueprint.route('/add-info', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        birthday = request.form['birthday']
        age = request.form['age']
        contactnumber = request.form['contactnumber']
        email = request.form['email']

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        cursor.execute('INSERT INTO tbl_project(firstname, middlename, lastname, birthday, age, contactnumber, email) VALUES (%s, %s, %s, %s, %s, %s, %s)', (firstname, middlename, lastname, birthday, age, contactnumber, email))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('blueprint.info'))
        
    else:
        return render_template('add.html')

@blueprint.route('/delete/<int:user_id>', methods=['GET', 'POST'])
def delete(user_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute('DELETE FROM tbl_project WHERE id = %s;', (user_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('blueprint.info'))



