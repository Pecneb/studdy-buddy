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
    print(request.user)
    if request.method == 'POST':
        print(request.form)
        subject_filter = request.form['subject']
        g.subject_filter = subject_filter
    subjects = db.session.execute(
        db.select(Subject)
    ).scalars()
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
    print(tutorings)
    return render_template('tutoring/tutoring.html', tutorings=tutorings, subjects=subjects)


@bp.route('/create-tutoring', methods=('GET', 'POST'))
@login_required
def create_tutoring():
    if request.method == 'POST':
        
        subject = request.form['subject']
        start_datetime = request.form['start_datetime']
        end_datetime = request.form['end_datetime']
        