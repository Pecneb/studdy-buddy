import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from studdybuddy.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        neptun = request.form['neptun']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        email = request.form['email']
        db = get_db()
        error = None

        if not neptun:
            error = 'Neptun is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'

        if error is None:
            try:
                db.exeute(
                    "INSERT INTO hallgato (neptun, firstname, lastname, email, password) VALUES (?, ?, ?, ?, ?)",
                    (neptun, firstname, lastname, email, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User with {neptun} neptun-code is already registered."
            else:
                return redirect(url_for("auth.login"))
        
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        neptun = request.form['neptun']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM hallgato WHERE neptun = ?', (neptun,)
        ).fetchone()

        if user is None:
            error = 'Incorrect neptun-code.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['neptun'] = user['neptun']
            # TODO: this will not return to the index page, rather to the users main page
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')



@bp.before_app_request
def load_logged_in_user():
    neptun = session.get('neptun')

    if neptun is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM hallgato WHERE neptun = ?', (neptun,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    # TODO: not sure where to redirect, there is no index yet, but who knows
    # if there will be none, then this should redirect to the /auth/login page
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)