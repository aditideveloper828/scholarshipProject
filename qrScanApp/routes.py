from flask import render_template, flash, redirect, jsonify, url_for, request
from qrScanApp import application
from qrScanApp.forms import LoginForm, RegistrationForm, DeleteForm, TimeForm
from qrScanApp import storage
from flask_login import current_user, login_user, logout_user, login_required
from qrScanApp.models import User, Log, Code
from werkzeug.urls import url_parse

complete_log = []
individual = {'person':''}

@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html',  title='Scanner')

@application.route('/trial', methods=['GET', 'POST'])
def trial():
    information = request.get_json()
    code = Code.query.filter_by(code=information["info"]).first()
    if code is not None:
        log = Log(identity=current_user.identity)
        storage.session.add(log)
        storage.session.commit()
        response = jsonify(success=True)
        return response
    else:
        return "Error"
    

@application.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(identity=form.identity.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@application.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(identity=form.identity.data, first_name=form.first_name.data, last_name=form.last_name.data, editor=form.editor.data)
        user.set_password(form.password.data)
        storage.session.add(user)
        storage.session.commit()
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)

@application.route('/userdelete', methods=['GET', 'POST'])
def userdelete():
    form = DeleteForm()
    if form.validate_on_submit():
        user = User.query.filter_by(identity=form.identity.data).first()
        storage.session.delete(user)
        storage.session.commit()
        return redirect(url_for('userdelete'))
    return render_template('delete.html', title='Delete', form=form)

@application.route('/time', methods=['GET', 'POST'])
def time():
    form = TimeForm()
    if form.validate_on_submit():
        all_log = Log.query.filter_by(identity=form.identity.data).all()
        global individual
        global complete_log
        individual['person'] = form.identity.data
        for log in all_log:
            complete_log.append({'time':log.timestamp})
            print(complete_log)
        return redirect(url_for('display'))
    return render_template('time.html', title='Time', form=form)

@application.route('/display', methods=['GET', 'POST'])
def display():
    global complete_log
    global individual
    return render_template('display.html', title="Display", complete_log=complete_log, individual=individual)

@application.errorhandler(500)
def internal_error(error):
    return "500 error - Internal Server Exception", 500
 
@application.errorhandler(400)
def notFound(error):
    return jsonify({
           "success": False, 
           "error": 400,
           "message": "bad request"
           }), 400 


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000, debug=True)
