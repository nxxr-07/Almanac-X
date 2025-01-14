from flask import Blueprint, render_template, request, flash, redirect , url_for
from flask_login import login_user, login_required, logout_user, current_user
from Website import views
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, Try again.', category='error')

        else:
            flash('Invalid Email',category='error')

            

    return render_template("login.html", user=0)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method=="POST":
        email = request.form.get('email')
        name = request.form.get('name')
        roll = request.form.get('rollno')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        course = request.form.get('course')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        if(len(email))<4:
            flash('Email Must be greater than 4 characters', category="error")
        elif len(name) < 2:
            flash('First Name Must be greater than 3 characters', category="error")
        elif int(roll) < 2000000:
            flash('Please Enter valid Roll Number', category="error")
        elif password1 != password2:
            flash('Passwords dont match', category="error")
        elif( len(password1))<7:
            flash('Password Must be greater than 7 characters', category="error")
        else:
            new_user = User(email=email, name = name,roll=roll, course=course, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            flash("Account Created", category="success")
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")