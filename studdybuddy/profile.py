from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from studdybuddy.db import DB as db, Student 
from studdybuddy.db import Subject, Post
from studdybuddy.auth import login_required
from sqlalchemy.exc import DBAPIError
from sqlalchemy import update

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def profile():
    try:
        user = db.session.get(Student, g.user.neptun)
        if request.method == 'POST':
            if 'modify' in request.form:
                #region start 1 - compact~~~~~
                #compact, but makes the user object dirty -> more database transactions
                
                # user.firstname = request.form["firstname"] if user.firstname != request.form["firstname"] else user.firstname
                # user.lastname = request.form["lastname"] if user.lastname != request.form["lastname"] else user.lastname
                # user.neptun = request.form["neptun"] if user.neptun != request.form["neptun"] else user.neptun
                # user.email = request.form["email"] if user.email != request.form["email"] else user.email
                # user.password = request.form["new_password"] if user.password != request.form["new_password"] else user.password
                
                #region end~~~~~
                
                
                
                #region start 2 - effective~~~~~
                #looks primitive, but more resource efficient and stupid user safe
                
                new_firstname = request.form["firstname"] if user.firstname != request.form["firstname"] else None
                new_lastname = request.form["lastname"] if user.lastname != request.form["lastname"] else None
                new_neptun = request.form["neptun"] if user.neptun != request.form["neptun"] else None
                new_email = request.form["email"] if user.email != request.form["email"] else None
                new_pswd = request.form["new_password"]
                
                if new_firstname != '' and new_firstname != None:
                    user.firstname = new_firstname
                    
                if new_lastname != '' and new_lastname != None:
                    user.lastname = new_lastname
                    
                if new_neptun != '' and new_neptun != None:
                    user.neptun = new_neptun
                    
                if new_email != '' and new_email != None:
                    user.email = new_email
                    
                if new_pswd != '' and new_pswd!=None:
                    user.password = new_pswd
                #region end~~~~~
                
                
                if len(db.session.dirty)>0:
                    db.session.commit()
                    flash("Changes saved","success")
                
            elif 'delete' in request.form:
                db.session.delete(user)
                print(db.session.deleted)
                db.session.commit()
                return render_template('auth/login.html')
            else:
                flash("POST method failed","error") 
        return render_template('profile/profile.html', profile=user)
    except DBAPIError as e:
        flash(e,"error")
        print(e)
