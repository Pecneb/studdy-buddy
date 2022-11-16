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
    error = None
    if request.method == 'POST':
        if 'subject' in request.form:
            subject_filter = request.form['subject']
        else: 
            subject_filter = 'all'
        g.subject_filter = subject_filter
        if 'tutoring_to_apply' in request.form:
            tutoring_to_apply = request.form['tutoring_to_apply']
            tutoring = Tutoring.query.filter_by(id=tutoring_to_apply).first()
            # participants = db.session.query(TutoringParticipant.student_neptun).filter_by(tutoring_id=tutoring_to_apply).all()
            # print(participants)
            # if g.user.neptun in participants:
            #     flash('You already applied for this tutoring session!')
            if tutoring is not None:
                if TutoringParticipant.query.filter_by(
                    student_neptun=g.user.neptun,
                    tutoring_id=tutoring.id,
                ).first() is None:
                    db.session.add(TutoringParticipant(student_neptun=g.user.neptun,tutoring_id=tutoring.id,))
                    db.session.commit()
                    flash('Application was successfull!', 'info')
                else:
                    flash('Already applied!', 'danger')
    subjects = db.session.execute(db.select(Subject)).scalars()
    filter = g.get('subject_filter')
    if filter == 'all' or filter is None:
        tutorings = db.session.execute(db.select(Tutoring).order_by(Tutoring.start_datetime)).scalars()
    else:
        tutorings = db.session.execute(db.select(Tutoring).where(Tutoring.subject_id==filter).order_by(Tutoring.start_datetime)).scalars()
    return render_template('tutoring/tutoring.html', tutorings=tutorings, subjects=subjects)

@bp.route('/create-tutoring', methods=('GET', 'POST'))
@login_required
def create_tutoring():
    if request.method == 'POST':
            tutor_neptun = g.user.neptun
            tutoring_name = request.form['tutoring_name']
            subject_id = request.form['subject']
            start_datetime = request.form['start_datetime']
            end_datetime = request.form['end_datetime']
            max_participants = request.form['max_participants']

            error = error_handler(tutoring_name, subject_id, start_datetime, end_datetime, max_participants)
            if error is not None:
                flash(error)
            else:
                try:
                    tutoring = Tutoring(
                        tutoring_name = tutoring_name,
                        subject_id = subject_id,
                        start_datetime = start_datetime,
                        end_datetime = end_datetime,
                        max_participants = max_participants,
                    )
                    db.session.add(tutoring)
                    db.session.commit()
                except DBAPIError as e:
                    print(e)
            return redirect(url_for('.findtutoring'))

    subjects = db.session.execute(
        db.select(Subject)
    ).scalars()
    return render_template('tutoring/create_tutoring.html', subjects=subjects)

def error_handler(tutoring_name, subject_id, start_datetime, end_datetime, max_participants):
    error = None
    if tutoring_name is None:
        error = "Tutoring name required."
    elif subject_id is None:
        error = "Subject selection is required."
    elif start_datetime is None:
        error = "Start datetime is required."
    elif end_datetime is None:
        error = "End datetime is required."
    elif max_participants is None:
        error = "Max participants is required."
    return error