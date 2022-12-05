from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from studdybuddy.db import DB as db 
from studdybuddy.db import Subject, Post, Relations,Student
from sqlalchemy import or_, and_
from studdybuddy.auth import login_required
from sqlalchemy.exc import DBAPIError

bp = Blueprint('findpartner', __name__, url_prefix='/findpartner')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def findpartner():
    if request.method == 'POST':
        if "contact" in request.form:
            print(request.form['contact'])
            user = db.session.get(Student, g.user.neptun)
            if request.form['contact'] != user.neptun:
                existing_relations=db.session.execute(
                    db.select(Relations).filter(
                        or_(Relations.neptun2 == user.neptun,
                            Relations.neptun1 == user.neptun))).scalars()
                is_exists=False
                for relation in existing_relations:
                    if (relation.neptun1 == user.neptun and
                        relation.neptun2 == request.form['contact']
                        ) or (
                        relation.neptun2 == user.neptun and
                        relation.neptun1 == request.form['contact']):
                            
                            is_exists=True
                            break
                            
                if not is_exists:
                    newrel=Relations(neptun1=g.user.neptun, neptun2=request.form['contact'])
                    db.session.add(newrel)
                    db.session.commit()
                return redirect(url_for('messages.chat', id=request.form['contact']))
        if "filter" in request.form:
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
    return render_template('find_partner/find_partner.html', posts=posts, tantargyak=tantargyak)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        tkod = request.form['tantargy']
        hallgato = g.user.neptun
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
            try:
                post = Post(
                    student_neptun=hallgato,
                    subject_id=tkod,
                    title=title,
                    body=body
                )
                db.session.add(post)
                db.session.commit()
            except DBAPIError as e:
                print(e)
        return redirect(url_for('.findpartner'))

    tantargyak = db.session.execute(
        db.select(Subject)
    ).scalars()
    return render_template('find_partner/create_post.html', tantargyak=tantargyak)