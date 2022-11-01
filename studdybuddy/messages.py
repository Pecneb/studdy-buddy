from email import message
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from studdybuddy.auth import login_required
from sqlalchemy.exc import DBAPIError
from sqlalchemy import or_, and_
from studdybuddy.db import DB as db, Message, Relations, Student
import string

bp = Blueprint('messages', __name__, url_prefix='/chats')

@bp.route('/list', methods=('GET', 'POST'))
@login_required
def chats():
    try:
        user = db.session.get(Student, g.user.neptun)
        if request.method == "POST":
            if 'tanulo' in request.form:
                existing_relations=db.session.execute(
                    db.select(Relations).filter(
                        or_(Relations.neptun2 == user.neptun,
                            Relations.neptun1 == user.neptun))).scalars()
                is_exists=False
                for relation in existing_relations:
                    if (relation.neptun1 == user.neptun and
                        relation.neptun2 == request.form['tanulo']
                        ) or (
                        relation.neptun2 == user.neptun and
                        relation.neptun1 == request.form['tanulo']):
                            
                            is_exists=True
                            break
                            
                if not is_exists:
                    newrel=Relations(neptun1=g.user.neptun, neptun2=request.form['tanulo'])
                    db.session.add(newrel)
                    db.session.commit()
            

        relations=db.session.execute(
            db.select(Relations).filter(
                or_(Relations.neptun2 == user.neptun,
                    Relations.neptun1 == user.neptun))).scalars()
        
        exclude_neptun=list()
        
        related_students=list()
        for relation in relations:
            if relation.neptun2 != user.neptun:
                stud=db.session.get(Student,relation.neptun2)
            elif relation.neptun1 != user.neptun:
                stud=db.session.get(Student,relation.neptun1)
            related_students.append(stud)
            exclude_neptun.append(stud.neptun)
        
        other_students=db.session.execute(
            db.select(Student)
            .where(Student.neptun != user.neptun).filter(~Student.neptun.in_(exclude_neptun))
        ).scalars()
        
        # db.session.commit()
        return render_template('chats/chat_list.html', 
                               other_students=other_students, 
                               related_students=related_students)
            
    except DBAPIError as e:
        flash(e,"error")
        print(e)
        return render_template('menu/index.html')
    
@bp.route('/<string:id>', methods=('GET', 'POST'))
@login_required
def chat(id: string):
    try:
        user = db.session.get(Student, g.user.neptun)
        partner=db.session.get(Student, id)
        relation=db.session.execute(
            db.select(Relations).where(  or_(and_(Relations.neptun1 == user.neptun, Relations.neptun2 == id),
                                             and_(Relations.neptun2 == user.neptun, Relations.neptun1 == id)) )
        ).one()[0]
        
        if request.method == "POST":
            if len(request.form['message'])>0:
                new_msg=Message(sender=user.neptun, message=request.form['message'], relation=relation.id)
                db.session.add(new_msg)
                db.session.commit()

        
        resp_messages=None
        
        messages=db.session.execute(
            db.select(Message).where(Message.relation == relation.id)
        ).all()
        
        print(messages)
        if len(messages)<=0:
            resp_messages=[{'message':"No messages yet."}]
        else:
            resp_messages=messages
        
        return render_template('chats/messages.html',messages=resp_messages, partner=partner)
    
    except DBAPIError as e:
        flash(e,"error")
        print(e)
        return render_template('menu/index.html')