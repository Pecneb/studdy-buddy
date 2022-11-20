from flask_admin.contrib.sqla import ModelView

class Base(ModelView):
    column_display_pk = True

class StudentModelView(Base):
    form_columns = ('neptun', 'firstname', 'lastname', 'password', 'email')

class PostModelView(Base):
    form_columns = ('id', 'student_neptun', 'subject_id', 'title', 'body', 'created')

class SubjectModelView(Base):
    form_columns = ('id', 'name')

class TutoringModelView(Base):
    form_columns = ('id', 'tutor_neptun', 'tutoring_name', 'subject_id', 'created', 'start_datetime', 'end_datetime')

class TutoringParticipantModelView(Base):
    form_columns = ('id', 'student_neptun', 'tutoring_id')

class GroupModelView(Base):
    form_columns = ('id', 'name', 'created')

class GroupMemberModelView(Base):
    form_columns = ('id', 'student_neptun', 'group_id')

class GroupPostModelView(Base):
    form_columns = ('group_id', 'group_member_id', 'body')