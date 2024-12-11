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

    usernamemsg = ''
    passwordmsg = ''
    msg = ''
    
    if request.method == 'POST':
        Username = request.form['Username']
        Password = request.form['Password']
        if Username != 'Raymund':
            usernamemsg = 'Username is incorrect!'

        if Password != '123456789':
            passwordmsg = 'Password is incorrect!'

        if not usernamemsg and not passwordmsg:
            try:
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()
                cursor.execute("INSERT INTO tbl_login (username, password) VALUES(%s, %s)", (Username, Password))  # Assuming you are inserting raw data
                connection.commit()
                session['user'] = Username
                return redirect(url_for('blueprint.dashboard'))
            except mysql.connector.Error as e:
                msg = f"Adding data failed! Error: {str(e)}"
            finally:
                cursor.close()
                connection.close()
        else:
            msg = usernamemsg or passwordmsg

    response = make_response(render_template('index.html', msg=msg, usernamemsg=usernamemsg, passwordmsg=passwordmsg))
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
    
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM tbl_project LIMIT 1')
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    response = make_response(render_template('profile.html', data=data))
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

@blueprint.route('/Add-Info', methods=['GET', 'POST'])
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

@blueprint.route('/Edit_Profile', methods=['GET', 'POST'])
def edit():

    try:

        if 'user' not in session or not session['user']:
            return redirect(url_for('blueprint.index'))
        
        ID = 43  

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
                "age": validate_age(age) if age is not None else "Age must be a valid number.",
                "contactnumber": validate_contact_number(form_data['contactnumber']),
                "email": validate_email(form_data['email']),
            }

            errors = {field: msg for field, msg in errors.items() if msg}

            if errors:
                response = make_response(render_template('edit.html', form_data=form_data, errors=errors))
                return make_header(response)
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            update_query = (
                "UPDATE tbl_project SET firstname=%s, middlename=%s, lastname=%s, birthday=%s, age=%s, contactnumber=%s, email=%s WHERE ID=%s"
            )
            update_values = (
                form_data['firstname'],
                form_data['middlename'],
                form_data['lastname'],
                form_data['birthday'],
                age,
                form_data['contactnumber'],
                form_data['email'],
                ID,
            )
            cursor.execute(update_query, update_values)
            conn.commit()
            cursor.close()
            conn.close()


            return redirect(url_for('blueprint.profile'))


        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        select_query = "SELECT * FROM tbl_project WHERE ID = %s"
        cursor.execute(select_query, (ID,))
        user_data = cursor.fetchone()


        form_data = {
            'firstname': user_data.get('firstname', '') if user_data else '',
            'middlename': user_data.get('middlename', '') if user_data else '',
            'lastname': user_data.get('lastname', '') if user_data else '',
            'birthday': user_data.get('birthday', '') if user_data else '',
            'age': user_data.get('age', '') if user_data else '',
            'contactnumber': user_data.get('contactnumber', '') if user_data else '',
            'email': user_data.get('email', '') if user_data else '',
        }

        cursor.close()
        conn.close()

        response = make_response(render_template('edit.html', form_data=form_data, errors={}))
        return make_header(response)

    except Exception as e:
        
        error_message = f"An unexpected error occurred: {str(e)}"
        form_data = {
            'firstname': '',
            'middlename': '',
            'lastname': '',
            'birthday': '',
            'age': '',
            'contactnumber': '',
            'email': ''
        }
        response = make_response(render_template('edit.html', form_data=form_data, errors={"general": error_message}))
        return make_header(response)
    
@blueprint.route('/update-page', methods=["GET"])
def update_page():
    return redirect(url_for('blueprint.edit'))

@blueprint.route('/Edit-User/<int:ID>', methods=['GET', 'POST'])
def edit_user(ID):

    try:

        if 'user' not in session or not session['user']:
            return redirect(url_for('blueprint.index'))

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
                "age": validate_age(age) if age is not None else "Age must be a valid number.",
                "contactnumber": validate_contact_number(form_data['contactnumber']),
                "email": validate_email(form_data['email']),
            }

            errors = {field: msg for field, msg in errors.items() if msg}

            if errors:
                response = make_response(render_template('edit-user.html', form_data=form_data, errors=errors))
                return make_header(response)
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            update_query = (
                "UPDATE tbl_project SET firstname=%s, middlename=%s, lastname=%s, birthday=%s, age=%s, contactnumber=%s, email=%s WHERE ID=%s"
            )
            update_values = (
                form_data['firstname'],
                form_data['middlename'],
                form_data['lastname'],
                form_data['birthday'],
                age,
                form_data['contactnumber'],
                form_data['email'],
                ID,
            )
            cursor.execute(update_query, update_values)
            conn.commit()
            cursor.close()
            conn.close()


            return redirect(url_for('blueprint.info'))


        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        select_query = "SELECT * FROM tbl_project WHERE ID = %s"
        cursor.execute(select_query, (ID,))
        user_data = cursor.fetchone()


        form_data = {
            'firstname': user_data.get('firstname', '') if user_data else '',
            'middlename': user_data.get('middlename', '') if user_data else '',
            'lastname': user_data.get('lastname', '') if user_data else '',
            'birthday': user_data.get('birthday', '') if user_data else '',
            'age': user_data.get('age', '') if user_data else '',
            'contactnumber': user_data.get('contactnumber', '') if user_data else '',
            'email': user_data.get('email', '') if user_data else '',
        }

        cursor.close()
        conn.close()

        response = make_response(render_template('edit-user.html', form_data=form_data, errors={}))
        return make_header(response)

    except Exception as e:
        
        error_message = f"An unexpected error occurred: {str(e)}"
        form_data = {
            'firstname': '',
            'middlename': '',
            'lastname': '',
            'birthday': '',
            'age': '',
            'contactnumber': '',
            'email': ''
        }
        response = make_response(render_template('edit-user.html', form_data=form_data, errors={"general": error_message}))
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



