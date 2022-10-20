from traceback import print_tb
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from studdybuddy.db import DB as db 
from studdybuddy.db import Group, Subject, GroupMember
from studdybuddy.auth import login_required
import sys
from sqlalchemy.exc import DBAPIError

bp = Blueprint('findgroup', __name__, url_prefix='/findgroup')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def findgroup():
    csoportok = db.session.execute(
        db.select(Group)
    ).scalars()

    tantargyak = db.session.execute(
        db.select(Subject)
    ).scalars()

    tagok = db.session.execute(
        db.select(GroupMember)
    ).scalars()


    csoportletszam = [0,0,0,0,0]
    for i in tagok:
        csoportletszam[i.group_id] += 1
    
    for y in csoportletszam:
        print(y, file=sys.stdout)
    return render_template('find_group/find_group.html', groups=csoportok, tantargyak=tantargyak, tagok=tagok)


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