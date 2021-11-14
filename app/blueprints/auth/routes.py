from flask import render_template, request, redirect, url_for, flash
import requests
# from .forms import PokemonForm, 
from .forms import LoginForm, RegisterForm, PasswordField, EditProfileForm
from wtforms.validators import EqualTo, DataRequired, ValidationError
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from . import bp as auth

@auth.route('/login', methods=['GET' , 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit:
        #do login stuff
        email = request.form.get('email').lower()
        password = request.form.get('password')

        u = User.query.filter_by(email=email).first()

        if u and u.check_hashed_password(password):
            login_user(u)
            #will want to give the user feedback saying successful login
            flash('You have logged in.', 'success')
            return redirect (url_for("main.index"))
        # else: #not necessary, could unindent the else statement, because of the return in the if statement
        # if email in app.config.get('REGISTERED_USERS') and \
        #     password == app.config.get('REGISTERED_USERS').get(email).get(password): THESE 3 LINES DEPRECATED BY U.CHECK_HASHED_PASSWORD
            # return f"Welcome, Pokemon trainer! {app.config.get('REGISTERED_USERS').get(email).get(name)}"
        error_string = flash("I think you may have come to the wrong place. We couldn't log you in with that info.", "danger")
        #!!!THERE IS AN ERROR BELOW!!!
        return redirect (url_for("auth.register"))
        # render_template('register.html.j2', error = error_string, form=form) 
    return render_template('login.html.j2', form = form)

@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash ("Farewell, trainer. You have been logged out.", 'danger')
        return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data,
                "icon":form.icon.data
                # "confirm_password":form.confirm_password.data,
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data) 
            #we just built a user with form data (1st line)
            #using the method in the user class to retrieve the data (2nd line)
            #save that user to the database, below
            new_user_object.save()
        except:
            error_string = "Beedrills got in our machine! Something went wront with your registration. Come back when we've caught them and patched up!"
            return render_template ('register.html.j2', form = form, error=error_string)
        return redirect(url_for('auth.login'))
    return render_template('register.html.j2', form = form)
    
@auth.route('/edit_profile', methods=['GET', "POST"])
def edit_profile():
    form = EditProfileForm()
    if request.method=='POST' and form.validate_on_submit():
        new_user_data={
            "first_name":form.first_name.data.title(),
            "last_name":form.last_name.data.title(),
            "email":form.email.data.lower(),
            "password":form.password.data,
            "icon":form.icon.data if int(form.icon.data)!=10000 else current_user.icon,
        }
        user=User.query.filter_by(email=form.email.data.lower()).first()
        if user and current_user.email != user.email:
            flash("Email already in use", "danger")
            return redirect(url_for('auth.edit_profile'))
        try:
            current_user.from_dict(new_user_data)
            current_user.save()
            flash("Pofile Updated", "success")
        except:
            flash("Beedrills got in our machine! Something went wront with your profile edit. Come back when we've caught them and patched up!", "danger")
            return redirect(url_for("auth.edit_profile"))

        
    return render_template("register.html.j2", form=form)