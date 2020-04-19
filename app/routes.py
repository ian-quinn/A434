import os, re, json

from flask import flash, render_template, send_from_directory, current_app, redirect, url_for, request
from flask import get_flashed_messages, g
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

# ------------from current app-------------
from app import app, db
from app.models import User, File
from app.forms import LoginForm, RegistrationForm

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('briefcase'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('briefcase')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('briefcase'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Request admitted! Please login', 'success')
        return redirect(url_for('briefcase'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('briefcase'))


@app.route('/briefcase')
def briefcase():
    #list = os.listdir(app.config['briefcase_PATH'])
    files = File.query.all()
    return render_template('briefcase.html', files=files)

@app.route('/briefcase/<int:file_id>/delete', methods=['POST'])
@login_required
def delete(file_id):
    file = File.query.get_or_404(file_id)
    file_path = os.path.join(app.config['FILE_PATH'], file.link)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.session.delete(file)
    db.session.commit()
    return redirect(url_for('briefcase'))

@app.route('/briefcase/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        for f in request.files.getlist('file'):
            name = f.filename
            # Skim out duplicated files
            if File.query.filter_by(name=name).first() is None:
                #surname = os.path.splitext(name)[0]
                bookend = os.path.splitext(name)[1]
                link = name

                path = os.path.join(app.config['FILE_PATH'], link)
                f.save(path)
                size = os.stat(path).st_size
                if size > 1000:
                    if size > 1000000:
                        size = str(round(size/1024/1024, 2)) + ' MB'
                    else:
                        size = str(int(size/1024)) + ' KB'
                else:
                    size = str(size) + ' B'

                file = File(name=name, link=link, size=size, bookend=bookend)
                db.session.add(file)
                db.session.commit()
    return ('', 204)