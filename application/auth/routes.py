from flask import render_template, flash, redirect, url_for, request
from application.auth.forms import LoginForm, ResetPasswordRequestForm, ResetPassword
from application.auth import bp
from application import db
from flask_login import current_user, login_user, logout_user, login_required
from application.models import User
from application.auth.email import send_reset_email
from werkzeug.urls import url_parse

@bp.route("/login", methods=["GET", "POST"])
def loginn():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form=LoginForm()
    if form.validate_on_submit():
#Checks to see if the username exists and if password exists too.
        user = User.query.filter_by(username=form.useremail.data).first()
        if user is None or not user.check_password(form.password.data):
            user = User.query.filter_by(email=form.useremail.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username biatch')
                return redirect(url_for('auth.loginn'))
        login_user(user, remember=form.remember_me.data)
#Now we do this to remember the redirects. netloc works so it doesnt redirect to outside sites inputted by the user.
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('main.index'))
        return redirect(next_page)
    return render_template("auth/login.html", title="Sign in", form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/resetpass', methods=['GET', 'POST'])
def resetpasscheck():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form=ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.loginn'))
    return render_template('auth/passreset.html', title='Reset Password', form=form)

@bp.route('/passwordreset/<token>', methods=['GET', 'POST'])
def resetpass(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user= User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form=ResetPassword()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.loginn'))
    return render_template('auth/passwordreset.html', form=form)
