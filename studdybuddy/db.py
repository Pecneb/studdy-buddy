from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class Student(DB.Model):
    __tablename__ = "student"
    neptun = DB.Column(DB.String(6), primary_key=True)
    firstname = DB.Column(DB.String(255), nullable=False)
    lastname = DB.Column(DB.String(255), nullable=False)
    password = DB.Column(DB.String(255), nullable=False)
    email = DB.Column(DB.String(255), nullable=False)

    group_members = relationship(
        "GroupMember", back_populates="student", cascade="all, delete-orphan"
    )

class Relations(DB.Model):
    id = DB.Column(DB.Integer, autoincrement=True, primary_key=True)
    neptun1 = DB.Column(DB.String(6), ForeignKey(Student.neptun), nullable=False)
    neptun2 = DB.Column(DB.String(6), ForeignKey(Student.neptun), nullable=False)
    is_buddies = DB.Column(DB.Boolean, default=False, nullable=False)

class Message(DB.Model):
    id = DB.Column(DB.Integer, autoincrement=True, primary_key=True)
    relation = DB.Column(DB.Integer, ForeignKey(Relations.id), nullable=False)
    sender=DB.Column(DB.String(6),ForeignKey(Student.neptun),nullable=False)
    message=DB.Column(DB.String(200),nullable=False)
    creationtime = DB.Column(DB.DateTime(timezone=True), default=datetime.now())

class Post(DB.Model):
    __tablename__ = "post"
    id = DB.Column(DB.Integer, autoincrement=True, primary_key=True)
    student_neptun = DB.Column(DB.String(6), ForeignKey("student.neptun"), nullable=False)
    subject_id = DB.Column(DB.String(255), ForeignKey("subject.id"), nullable=False)
    title = DB.Column(DB.String(30), nullable=False)
    body = DB.Column(DB.String(500), nullable=False)
    created = DB.Column(DB.DateTime(timezone=True), default=datetime.now())

    @hybrid_property
    def subject_name(self):
        obj = Subject.query.filter_by(id=self.subject_id).first()
        return obj.name

class Subject(DB.Model):
    __tablename__ = "subject"
    id = DB.Column(DB.String(255), primary_key=True)
    name = DB.Column(DB.String(255), nullable=False)

class Tutoring(DB.Model):
    __tablename__ = "tutoring"
    id = DB.Column(DB.Integer, autoincrement=True, primary_key=True)
    tutor_neptun = DB.Column(DB.String(6), ForeignKey("student.neptun"), nullable=False)
    tutoring_name = DB.Column(DB.String(255), nullable=False)
    subject_id = DB.Column(DB.String(255), ForeignKey("subject.id"), nullable=False)
    created = DB.Column(DB.DateTime(timezone=True), default=datetime.now())
    start_datetime = DB.Column(DB.DateTime(timezone=True), default=datetime.utcnow())
    end_datetime = DB.Column(DB.DateTime(timezone=True), nullable=False)
    max_participants = DB.Column(DB.Integer, nullable=False)

    @hybrid_property
    def tutor_name(self):
        obj = Student.query.filter_by(neptun=self.tutor_neptun).first()
        return obj.firstname + " " + obj.lastname

    @hybrid_property
    def subject_name(self):
        obj = Subject.query.filter_by(id=self.subject_id).first()
        return obj.name

class TutoringParticipant(DB.Model):
    __tablename__ = "tutoring_participant"
    id = DB.Column(DB.Integer, autoincrement=True, primary_key=True)
    student_neptun = DB.Column(DB.String(6), ForeignKey("student.neptun"), nullable=False)
    tutoring_id = DB.Column(DB.Integer, ForeignKey("tutoring.id"), nullable=False)

class Group(DB.Model):
    __tablename__ = "group"
    id = DB.Column(DB.Integer, autoincrement=True, primary_key=True)
    name = DB.Column(DB.String(255), nullable=False)
    created = DB.Column(DB.DateTime(timezone=True), default=datetime.now())
    team_size = DB.Column(DB.Integer, nullable=False)

    group_members = relationship(
        "GroupMember", back_populates="group", cascade="all, delete-orphan" 
    )
    group_posts = relationship(
        "GroupPost", back_populates="group", cascade="all, delete-orphan"
    ) 
    group_requests = relationship(
        "GroupRequests", back_populates="group", cascade="all, delete-orphan"
    )

    def __init__(self, name, desc, team_size, cneptun, sub_id):
        self.name = name
        self.desc = desc
        self.team_size = team_size
        self.creator_neptun = cneptun
        self.subject_id = sub_id

class GroupMember(DB.Model):
    __tablename__ = "group_member"
    id = DB.Column(DB.Integer, autoincrement=True, primary_key=True)
    student_neptun = DB.Column(DB.String(6), ForeignKey("student.neptun"), nullable=False)
    group_id = DB.Column(DB.Integer, ForeignKey("group.id"), nullable=False)
    admin = DB.Column(DB.Boolean, default=False, nullable=False)

    student = relationship(
        "Student", back_populates="group_members"
    )
    group = relationship(
        "Group", back_populates="group_members"
    )
    group_posts = relationship(
        "GroupPost", back_populates="member", cascade="all, delete-orphan"
    )

    def __init__(self, student_neptun, group_id, admin=False):
        self.student_neptun = student_neptun
        self.group_id = group_id
        self.admin = admin

class GroupPost(DB.Model):
    __tablename__ = "group_post"
    id = DB.Column(DB.Integer, autoincrement=True, primary_key=True)
    group_member_id = DB.Column(DB.Integer, ForeignKey("group_member.id"), nullable=False)
    group_id = DB.Column(DB.Integer, ForeignKey("group.id"), nullable=False)
    body = DB.Column(DB.String(500), nullable=False)

    group = relationship(
        "Group", back_populates="group_posts"
    )
    member = relationship(
        "GroupMember", back_populates="group_posts"
    )

    def __init__(self, group_id, group_member_id, body):
        self.group_id = group_id
        self.group_member_id = group_member_id
        self.body = body

class GroupRequests(DB.Model):
    __tablename__ = "group_requests"
    id = DB.Column(DB.Integer, autoincrement=True, primary_key=True)
    group_id = DB.Column(DB.Integer, ForeignKey("group.id"), nullable=False)
    sender = DB.Column(DB.String(6), ForeignKey("student.neptun"), nullable=False)
    message = DB.Column(DB.String(500), nullable=False)

    group = relationship(
        "Group", back_populates="group_requests"
    )

    def __init__(self, group_id, sender_neptun, message):
        self.group_id = group_id
        self.sender = sender_neptun
        self.message = message
