from flask import render_template, flash, redirect, jsonify, url_for, request
from qrScanApp import application
from qrScanApp.forms import LoginForm, RegistrationForm, AdminLoginForm, AdminRegistrationForm, DeleteForm, AdminDeleteForm
from qrScanApp import storage
from flask_login import current_user, login_user, logout_user, login_required
from qrScanApp.models import User, Log, Code, Admin
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
        user = User.query.filter_by(student_id=form.student_number.data).first()
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
        user = User(student_id=form.student_id.data, first_name=form.first_name.data, last_name=form.last_name.data)
        user.set_password(form.password.data)
        storage.session.add(user)
        storage.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@application.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(teacher_code=form.teacher_code.data).first()
        if admin is None or not admin.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('adminlogin'))
        login_user(admin, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('adminlogin.html', title='Admin Login', form=form)

@application.route('/adminregister', methods=['GET', 'POST'])
def adminregister():
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        admin = Admin(teacher_code=form.teacher_code.data, first_name=form.first_name.data, last_name=form.last_name.data)
        admin.set_password(form.password.data)
        storage.session.add(admin)
        storage.session.commit()
        return redirect(url_for('adminlogin'))
    return render_template('adminregister.html', title='Admin Register', form=form)

@application.route('/studentdelete', methods=['GET', 'POST'])
def studentdelete():
    form = DeleteForm()
    if form.validate_on_submit():
        user = User.query.filter_by(student_id=form.student_id.data).first()
        storage.session.delete(user)
        storage.session.commit()
        return redirect(url_for('studentdelete'))
    return render_template('delete.html', title='Delete Student', form=form)

@application.route('/admindelete', methods=['GET', 'POST'])
def admindelete():
    form = AdminDeleteForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(teacher_code=form.teacher_code.data).first()
        storage.session.delete(admin)
        storage.session.commit()
        return redirect(url_for('admindelete'))
    return render_template('admindelete.html', title='Delete Admin', form=form)

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
