from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from studdybuddy.db import DB as db 
from studdybuddy.db import Subject, Tutoring, TutoringParticipant
from studdybuddy.auth import login_required
from sqlalchemy.exc import DBAPIError

bp = Blueprint('findtutoring', __name__, url_prefix='/findtutoring')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def findtutoring():
    if request.method == 'POST':
        subject_filter = request.form['tantargy']
        g.subject_filter = subject_filter
    subjects = db.session.execute(
        db.select(Subject)
    ).scalars()
    print(subjects.all())
    filter = g.get('subject_filter')
    if filter == 'all' or filter is None:
        tutorings = db.session.execute(
            db.select(Tutoring)
            .order_by(Tutoring.start_datetime)
        ).scalars()
    else:
        tutorings = db.session.execute(
            db.select(Tutoring)
            .where(Tutoring.subject_id==filter)
            .order_by(Tutoring.start_datetime)
        ).scalars()
    return render_template('tutoring/tutoring.html', tutorings=tutorings, subjects=subjects)