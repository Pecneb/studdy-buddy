from sqlite3 import Error
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from studdybuddy.db import get_db
from studdybuddy.auth import login_required

bp = Blueprint('findpartner', __name__, url_prefix='/findpartner')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def findpartner():
    db = get_db()
    if request.method == 'POST':
        tfilter = request.form['tantargy']
        g.tfilter = tfilter
    # Query classes from db
    tantargyak = db.execute(
        'SELECT tkod, tnev FROM tantargy'
    ).fetchall()
    # Query posts from db
    filt = g.get('tfilter')
    if filt is not None:
        posts = db.execute(
            'SELECT p.title, p.body, strftime("%Y-%m-%d %H:%M:%S", p.created) "created", h.firstname + ' ' + h.lastname as "hallgatonev", t.tnev' 
            ' FROM post p JOIN hallgato h ON p.hallgatoneptun = h.neptun'
            ' JOIN tantargy t ON t.tkod = p.tkod'
            ' WHERE p.tkod=?'
            ' ORDER BY created DESC',
            (filt,)
        ).fetchall()
    else:
        posts = db.execute(
            'SELECT p.title, p.body, strftime("%Y-%m-%d %H:%M:%S", p.created) "created", h.firstname + ' ' + h.lastname as "hallgatonev", t.tnev' 
            ' FROM post p JOIN hallgato h ON p.hallgatoneptun = h.neptun'
            ' JOIN tantargy t ON t.tkod = p.tkod'
            ' ORDER BY created DESC',
        ).fetchall()
    g.tfilter = None
    return render_template('find_partner/find_partner.html', posts=posts, tantargyak=tantargyak)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        tkod = request.form['tantargy']
        hallgato = g.user['neptun']
        error = None

        if title is None:
            error = "Title required."
        elif body is None:
            error = "Text body required."
        elif tkod is None:
            error = "Subject selection is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            try:
                db.execute(
                    'INSERT INTO post(hallgatoneptun,tkod,title,body) values(?,?,?,?)',
                    (hallgato, tkod, title, body,)
                )
                db.commit()
            except Error as e:
                print(e)
            pass
        redirect(url_for('findpartner.findpartner'))

    db = get_db()
    tantargyak = db.execute(
        'SELECT * FROM tantargy'
    ).fetchall()
    return render_template('find_partner/create_post.html', tantargyak=tantargyak)