import re
from sqlite3 import Error
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from studdybuddy.db import get_db
from studdybuddy.auth import login_required
import sys

bp = Blueprint('findgroup', __name__, url_prefix='/findgroup')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def findgroup():

    db = get_db()
    csoportok = db.execute(
        'SELECT * FROM csoport'
    ).fetchall()

    tantargyak = db.execute(
        'SELECT * FROM tantargy'
    ).fetchall()

    # Query classes from db
    tantargyak = db.execute('SELECT tkod, tnev FROM tantargy').fetchall()

    return render_template('find_group/find_group.html', groups=csoportok, tantargyak=tantargyak)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_group():
    db = get_db()

    tantargyak = db.execute(
        'SELECT * FROM tantargy'
    ).fetchall()

    if request.method == 'POST':
        name = request.form['title']
        desc = request.form['description']
        tkod = request.form['tantargy']
        team_size = request.form['team_size']
        creatorneptun = g.user['neptun']
        error = None

        print('[*] POSTING TO DB:' + name +', '+ desc +', '+ tkod +', '+ team_size +', '+ creatorneptun, file=sys.stdout)

        if name is None:
            error = "Name required."
        elif desc is None:
            error = "Description required."
        elif tkod is None:
            error = "Subject selection is required."
        elif team_size is None:
            error = "Subject selection is required."
        
        if error is not None:
                flash(error)
        else:
            try:
                db.execute(
                    'INSERT INTO csoport(name, desc, team_size, creatorneptun, tkod) values(?,?,?,?,?)',
                    (name, desc, team_size, creatorneptun, tkod)
                )
                db.commit()
            except Error as e:
                print(e, file=sys.stdout)
            pass
        redirect(url_for('findgroup.findgroup'))

    return render_template('find_group/create_group.html', tantargyak=tantargyak)