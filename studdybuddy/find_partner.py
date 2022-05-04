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

@bp.route('/createpost', methods=('GET', 'POST'))
@login_required
def create_post():
    if request.method == 'POST':
        pass
    return render_template('find_partner/create_post.html')