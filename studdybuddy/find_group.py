from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from studdybuddy.db import DB as db 
from studdybuddy.db import Group, Subject, GroupMember, Student 
from studdybuddy.auth import login_required
import sys
from sqlalchemy.exc import DBAPIError

bp = Blueprint('findgroup', __name__, url_prefix='/findgroup')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def findgroup():
    if request.method == 'POST':
        pass
    csoportok = db.session.execute(
        db.select(Group)
    ).scalars()
    
    tantargyak = db.session.execute(
        db.select(Subject)
    ).scalars()
    
    csoport_letszamok = []
    for cs in csoportok:
        csoport_letszamok.append(
            len(db.session.execute(
                db.select(GroupMember)
                .where(GroupMember.group_id == cs.id)
            ).scalars().all())
        )

    csoportok = db.session.execute(
        db.select(Group)
    ).scalars()

    return render_template('find_group/find_group.html', groups=csoportok, tantargyak=tantargyak, letszamok=csoport_letszamok)



@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_group():
    tantargyak = db.session.execute(
        db.select(Subject)
    ).scalars()

    if request.method == 'POST':
        name = request.form['title']
        desc = request.form['description']
        tkod = request.form['tantargy']
        team_size = request.form['team_size']
        creatorneptun = g.user.neptun
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
                group = Group(name, desc, team_size, creatorneptun, tkod)
                db.session.add(group)
                db.session.flush()
                creator = GroupMember(g.user.neptun, group.id, 1)
                db.session.add(creator)
                db.session.commit()
            except DBAPIError as e:
                print(e, file=sys.stdout)

        return redirect(url_for('findgroup.findgroup'))
    return render_template('find_group/create_group.html', tantargyak=tantargyak)

@bp.route('/group/<int:id>', methods=('GET', 'POST'))
@login_required
def group_view(id: int):
    group = db.session.execute(
        db.select(Group)
        .where(Group.id == id)
    ).scalar()
    group_members = db.session.execute(
        db.select(Student)
        .where(GroupMember.group_id == id)
        .where(GroupMember.student_neptun == Student.neptun)
    ).scalars()
    if request.method == 'POST':
        if g.user in group_members:
            #TODO create post
            pass
        else:
            #TODO send message
            pass
    return render_template('find_group/view_group.html', group=group, group_members=group_members)