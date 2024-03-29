from flask import Blueprint, render_template, redirect, url_for, flash, abort
from . import auth
from .. import main
from ..models import User
from .forms import RegistrationForm, LoginForm
from .. import db
from flask_login import login_user, logout_user, login_required, current_user
from ..email import welcome_message

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember.data)

            return redirect(url_for('main.home'))

        flash('Invalid username or password')

    return render_template('auth/login.html', form=form)


@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created!', 'success')

        welcome_message("Welcome to the My Blog","email/welcome",user.email,user=user)

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


#Logout function
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))