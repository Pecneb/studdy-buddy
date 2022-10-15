from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

# Create the extension
DB = SQLAlchemy()

# Define Models
class Student(DB.Model):
    __tablename__ = "student"
    neptun = DB.Column(DB.String(6), primary_key=True)
    firstname = DB.Column(DB.String(255), nullable=False)
    lastname = DB.Column(DB.String(255), nullable=False)
    password = DB.Column(DB.String(255), nullable=False)
    email = DB.Column(DB.String(255), nullable=False)

class Post(DB.Model):
    __tablename__ = "post"
    id = DB.Column(DB.Integer, autoincrement=True, primary_key=True)
    student_neptun = DB.Column(DB.String(6), ForeignKey("student.neptun"), nullable=False)
    subject_id = DB.Column(DB.String(255), ForeignKey("subject.id"), nullable=False)
    title = DB.Column(DB.String(30), nullable=False)
    body = DB.Column(DB.String(500), nullable=False)
    created = DB.Column(DB.DateTime(timezone=True), default=datetime.now())

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
    start_datetime = DB.Column(DB.DateTime(timezone=True), default=datetime.now())
    end_datetime = DB.Column(DB.DateTime(timezone=True), nullable=False)

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

class GroupMember(DB.Model):
    __tablename__ = "group_member"
    id = DB.Column(DB.Integer, autoincrement=True, primary_key=True)
    student_neptun = DB.Column(DB.String(6), ForeignKey("student.neptun"), nullable=False)
    group_id = DB.Column(DB.Integer, ForeignKey("group.id"), nullable=False)