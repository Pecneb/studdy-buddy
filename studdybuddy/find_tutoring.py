from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from studdybuddy.db import DB as db 
from studdybuddy.db import Subject, Post
from studdybuddy.auth import login_required
from sqlalchemy.exc import DBAPIError

bp = Blueprint('findtutor', __name__, url_prefix='/findtutor')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def findtutoring():
    if request.method == 'POST':
        tfilter = request.form['tantargy']
        g.tfilter = tfilter
    # Query classes from db
    tantargyak = db.session.execute(
        db.select(Subject)
    ).scalars()
    # Query posts from db
    filt = g.get('tfilter')
    if filt == 'all' or filt is None:
        posts = db.session.execute(
            db.select(Post)
            .order_by(Post.created)
        ).scalars()
    else:
        posts = db.session.execute(
            db.select(Post)
            .where(Post.subject_id==filt)
            .order_by(Post.created)
        ).scalars()
    return render_template('tutoring/tutoring.html', posts=posts, tantargyak=tantargyak)