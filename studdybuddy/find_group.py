from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from studdybuddy.db import DB as db, GroupRequests 
from studdybuddy.db import Group, Subject, GroupMember, Student, GroupPost
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
        .join(GroupMember)
    ).scalars().all()
    group_posts = db.session.execute(
        db.select(GroupPost)
        .join(Group)
        .where(GroupPost.group_id==group.id)
    ).scalars()
    group_posters = db.session.execute(
        db.select(Student)
        .join(GroupMember.group_posts)
        .join(GroupMember.student)
    ).scalars().all()
    group_admins = db.session.execute(
        db.select(Student)
        .join(GroupMember)
        .where(GroupMember.admin == True)
    ).scalars()
    group_requests = db.session.execute(
        db.select(GroupRequests, Student)
        .select_from(GroupRequests)
        .join(Group)
        .where(GroupRequests.sender == Student.neptun)
        .where(GroupRequests.group_id == id)
    ).all()
    if request.method == 'POST':
        if g.user in group_members:
            if "invite_submit" in request.form:
                neptun = request.form["invite_submit"]

                student_to_add = db.session.execute(
                    db.select(Student)
                    .where(Student.neptun == neptun)
                ).scalar()
                student_as_groupmember = GroupMember(student_to_add.neptun, group.id, 0)
                
                group_request = None
                for req in group_requests:
                    print(req)
                    if req[0].sender == student_to_add.neptun:
                        group_request = req[0]

                try: 
                    db.session.add(student_as_groupmember)
                    db.session.delete(group_request)
                    db.session.commit()
                except DBAPIError as e:
                    print(e)
            if "post_submit" in request.form:
                body = request.form['body']

                error = None 

                if body is None:
                    error = "Post must have text in it."

                if error is None:
                    post_creator = db.session.execute(
                        db.select(GroupMember)
                        .where(GroupMember.group_id == id)
                        .where(GroupMember.student_neptun == g.user.neptun)
                    ).scalar()

                    post = GroupPost(id, post_creator.id, body)

                    try:
                        db.session.add(post)
                        db.session.commit()
                    except DBAPIError as e:
                        print(e)
                else:
                    flash(error)
        else:
            request_message = request.form['request']
            error = None 
            if request_message is None:
                error = "Request must have text in it."
            if error is None:
                request_message = GroupRequests(id, g.user.neptun, request_message)
                try:
                    db.session.add(request_message)
                    db.session.commit()
                except DBAPIError as e:
                    print(e)
            else:
                flash(error)
        return redirect(url_for('findgroup.group_view', id=id))
    return render_template('find_group/view_group.html', group=group, 
        group_members=group_members, group_posts=group_posts, group_posters=group_posters, 
        group_admins=group_admins, group_requests=group_requests
    )
