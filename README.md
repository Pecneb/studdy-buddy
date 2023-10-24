# studdy-buddy
Study partner and group finder, for University Students.

## Install

```
python3 -m pip install -r requirements.txt
```

## Initialize DB

DB management done with Flask-Migration tool

```
rm -r migrations/
```

```
flask --app studdybuddy db init
  Creating directory /media/pecneb/970evoplus/gitclones/studdy-buddy/migrations ...  done
  Creating directory /media/pecneb/970evoplus/gitclones/studdy-buddy/migrations/versions ...  done
  Generating /media/pecneb/970evoplus/gitclones/studdy-buddy/migrations/README ...  done
  Generating /media/pecneb/970evoplus/gitclones/studdy-buddy/migrations/alembic.ini ...  done
  Generating /media/pecneb/970evoplus/gitclones/studdy-buddy/migrations/env.py ...  done
  Generating /media/pecneb/970evoplus/gitclones/studdy-buddy/migrations/script.py.mako ...  done
  Please edit configuration/connection/logging settings in '/media/pecneb/970evoplus/gitclones/studdy-buddy/migrations/alembic.ini' before proceeding.
```

```
flask --app studdybuddy db migrate -m "Initial migration."
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'group'
INFO  [alembic.autogenerate.compare] Detected added table 'student'
INFO  [alembic.autogenerate.compare] Detected added table 'subject'
INFO  [alembic.autogenerate.compare] Detected added table 'group_member'
INFO  [alembic.autogenerate.compare] Detected added table 'group_requests'
INFO  [alembic.autogenerate.compare] Detected added table 'post'
INFO  [alembic.autogenerate.compare] Detected added table 'relations'
INFO  [alembic.autogenerate.compare] Detected added table 'tutoring'
INFO  [alembic.autogenerate.compare] Detected added table 'group_post'
INFO  [alembic.autogenerate.compare] Detected added table 'message'
INFO  [alembic.autogenerate.compare] Detected added table 'tutoring_participant'
  Generating /media/pecneb/970evoplus/gitclones/studdy-buddy/migrations/versions/5fef4fd2d302_initial_migration.py ...  done
```

```
flask --app studdybuddy db upgrade
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 5fef4fd2d302, Initial migration.
```

## Run server

```
flask --app studdybuddy run
```