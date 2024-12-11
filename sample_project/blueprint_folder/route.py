from flask import Flask, Blueprint, redirect, render_template, url_for, session, request, make_response
from .util.validation import validate_first_name,validate_middle_name,validate_last_name,validate_age,validate_birthday,validate_contact_number,validate_email
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

@blueprint.route('/add-info', methods=['GET', 'POST'])
def add():

    if request.method == "POST":
        
        form_data = {
            'firstname': request.form.get('firstname', '').strip(),
            'middlename': request.form.get('middlename', '').strip(),
            'lastname': request.form.get('lastname', '').strip(),
            'birthday': request.form.get('birthday', '').strip(),
            'age': request.form.get('age', '').strip(),
            'contactnumber': request.form.get('contactnumber', '').strip(),
            'email': request.form.get('email', '').strip(),
        }


        age = int(form_data['age']) if form_data['age'].isdigit() else None


        errors = {
            "firstname": validate_first_name(form_data['firstname']),
            "middlename": validate_middle_name(form_data['middlename']),
            "lastname": validate_last_name(form_data['lastname']),
            "birthday": validate_birthday(form_data['birthday'], age) if form_data['birthday'] and age else "Birthday and age are required.",
            "age": validate_age(age) if age else "Age must be a valid number.",
            "contactnumber": validate_contact_number(form_data['contactnumber']),
            "email": validate_email(form_data['email']),
        }

        errors = {field: msg for field, msg in errors.items() if msg}

        if not errors:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tbl_project WHERE email = %s", (form_data['email'],))
                if cursor.fetchone():
                    errors['email'] = "Email has already been registered."
                cursor.close()
                conn.close()
            except Exception as e:
                errors['general'] = f"Unexpected database error: {str(e)}"

        if errors:
            response = make_response(render_template('add.html', form_data=form_data, errors=errors))
            return make_header(response)

        try:
            conn = connect_db()
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO tbl_project (firstname, middlename, lastname, birthday, age, contactnumber, email)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                form_data['firstname'], form_data['middlename'], form_data['lastname'],
                form_data['birthday'], age, form_data['contactnumber'], form_data['email']
            ))
            conn.commit()
            cursor.close()
            conn.close()

            response = make_response(redirect(url_for('blueprint.info')))
            return make_header(response)

        except Exception as e:
            errors['general'] = f"Unexpected error during insertion: {str(e)}"
            response = make_response(render_template('add.html', form_data=form_data, errors=errors))
            return make_header(response)

    
    form_data = {
        'firstname': '',
        'middlename': '',
        'lastname': '',
        'birthday': '',
        'age': '',
        'contactnumber': '',
        'email': '',
    }
    response = make_response(render_template("add.html", form_data=form_data, errors={}))
    return make_header(response)


@blueprint.route('/delete/<int:user_id>', methods=['GET', 'POST'])
def delete(user_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute('DELETE FROM tbl_project WHERE id = %s;', (user_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('blueprint.info'))



