from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from studdybuddy.db import DB as db 
from studdybuddy.db import Subject, Tutoring, TutoringParticipant
from studdybuddy.auth import login_required
from sqlalchemy.exc import DBAPIError
import datetime

bp = Blueprint('findtutoring', __name__, url_prefix='/findtutoring')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def findtutoring():
    error = None
    if request.method == 'POST':
        if 'subject' in request.form:
            subject_filter = request.form['subject_id']
        else: 
            subject_filter = 'all'
        g.subject_filter = subject_filter
        if 'tutoring_to_delete' in request.form:
            tutoring_to_delete = request.form['tutoring_to_delete']
            print(tutoring_to_delete)
            tutoring = Tutoring.query.filter_by(id=tutoring_to_delete).first()
            if tutoring is not None:
                db.session.delete(tutoring)
                db.session.commit()
                flash('Tutoring was deleted!', 'success')
        if 'tutoring_to_apply' in request.form:
            tutoring_to_apply = request.form['tutoring_to_apply']
            tutoring = Tutoring.query.filter_by(id=tutoring_to_apply).first()
            if tutoring is not None:
                if TutoringParticipant.query.filter_by(
                    student_neptun=g.user.neptun,
                    tutoring_id=tutoring.id,
                ).first() is None:
                    db.session.add(TutoringParticipant(student_neptun=g.user.neptun,tutoring_id=tutoring.id,))
                    db.session.commit()
                    flash('Application was successfull!', 'success')
                else:
                    flash('Already applied!', 'error')
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
    _SUBJECTS = db.session.execute(
        db.select(Subject)
    ).scalars()
    if request.method == 'POST':
            tutor_neptun = g.user.neptun
            tutoring_name = request.form['tutoring_name']
            subject_id = request.form['subject_id']
            if 'start_datetime' in request.form and request.form['start_datetime'] != '':
                year, month, day, hour, minute = create_datetime(request.form['start_datetime'])
                start_datetime = datetime.datetime(year, month, day, hour, minute)
            else:
                start_datetime = None
            end_year, end_month, end_day, end_hour, end_minute = create_datetime(request.form['end_datetime'])
            end_datetime = datetime.datetime(end_year, end_month, end_day, end_hour, end_minute)

            date_error = None
            if start_datetime is not None:
                date_error = end_datetime < start_datetime
            else:
                date_error = end_datetime < datetime.datetime.now()

            max_participants = request.form['max_participants']

            error = error_handler(tutoring_name, subject_id, end_datetime, max_participants)
            if error is not None:
                flash(error)
            elif date_error:
                flash('Please provide valid date interval!', 'warning')
            else:
                try:
                    tutoring = Tutoring(
                        tutor_neptun=tutor_neptun,
                        tutoring_name = tutoring_name,
                        subject_id = subject_id,
                        end_datetime = end_datetime,
                        max_participants = max_participants,
                    )
                    if request.form['start_datetime'] != '':
                        tutoring.start_datetime = start_datetime
                    db.session.add(tutoring)
                    db.session.commit()
                    return redirect(url_for('.findtutoring'))
                except DBAPIError as e:
                    print(e)
    return render_template('tutoring/create_tutoring.html', subjects=_SUBJECTS)


def error_handler(tutoring_name, subject_id, end_datetime, max_participants):
    error = None
    if tutoring_name is None:
        error = "Tutoring name required."
    elif subject_id is None:
        error = "Subject selection is required."
    elif end_datetime is None:
        error = "End datetime is required."
    elif max_participants is None:
        error = "Max participants is required."
    return error

def create_datetime(date_string):
    date_string_split = date_string.split('T')
    date_split = date_string_split[0].split('-')
    year, month, day = int(date_split[0]), int(date_split[1]), int(date_split[2])
    date_time_split = date_string_split[1].split(':')
    hour = int(date_time_split[0])
    minute = int(date_time_split[1])
    return year, month, day, hour, minute