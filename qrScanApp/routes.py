from flask import render_template, flash, redirect, jsonify, url_for, request
from qrScanApp import application
from qrScanApp.forms import LoginForm, RegistrationForm, DeleteForm
from qrScanApp import storage
from flask_login import current_user, login_user, logout_user, login_required
from qrScanApp.models import User, Log, Code
from werkzeug.urls import url_parse



@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html',  title='Scanner')

@application.route('/trial', methods=['GET', 'POST'])
def trial():
    information = request.json("")
    if information == "http":
        return "1"
    else:
        return "2"
    #if request.method == 'POST':
    #    information = request.json()
    #    log = Log(student=17529)
    #    storage.session.add(log)
    #    storage.session.commit()
    #    return redirect(url_for('index'))
    #else:
    #    return redirect(url_for('register'))    

    

@application.route('/login', methods=['GET', 'POST'])
def login():
    #if request.method == 'POST':
    #    info = ""
    #    info = request.json()
    #    print(info)
        #check = Code.query.filter_by(code=info).first()
    #    log = Log(student=17529)
    #    storage.session.add(log)
    #    storage.session.commit()
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
