from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from studdybuddy.db import get_db
from studdybuddy.auth import login_required

bp = Blueprint('findpartner', __name__, url_prefix='/findpartner')

@bp.route('/')
@login_required
def findpartner():
    db = get_db()
    # Query classes from db
    tantargyak = db.execute(
        'SELECT tnev FROM tantargy'
    ).fetchall()
    # Query posts from db
    posts = db.execute(
        'SELECT p.body, p.created, h.firstname + ' ' + h.lastname as "hallgatonev", t.tnev' 
        ' FROM post p JOIN hallgato h ON p.hallgatoneptun = h.neptun'
        ' JOIN tantargy t ON t.tkod = p.tkod'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('find_partner/find_partner.html', posts=posts, tantargyak=tantargyak)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        hallgato = g.user['neptun']
        error = None

        if title is None:
            error = "Title required."
        elif body is None:
            error = "Text body required."

        if error is not None:
            flash(error)
        else:
            pass
        redirect(url_for('findpartner.findpartner'))
    return render_template('find_partner/create_post.html')