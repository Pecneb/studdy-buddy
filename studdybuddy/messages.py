from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from studdybuddy.auth import login_required
from sqlalchemy.exc import DBAPIError
from studdybuddy.db import DB as db, Student

bp = Blueprint('messages', __name__, url_prefix='/chats')

@bp.route('/list', methods=('GET'))
@login_required
def chats():
    try:
        user = db.session.get(Student, g.user.neptun)
        if request.method == 'GET':
            pass
        else:
            flash("Method error: Wrong method.","error")
            
    except DBAPIError as e:
        flash(e,"error")
        print(e)

    