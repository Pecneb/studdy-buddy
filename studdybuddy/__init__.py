import os
from flask import Flask, render_template

def page_not_found(e):
  return render_template('404.html'), 404

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'studdybuddy.db')}",
    )

    if test_config is None:
        # load the instance config, if it exist, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_error_handler(404, page_not_found)

    from . import db
    db.DB.init_app(app)
    with app.app_context():
        db.DB.create_all()

    from . import auth
    app.register_blueprint(auth.bp)

    from . import menu
    app.register_blueprint(menu.bp)
    app.add_url_rule('/', endpoint='index')

    from . import find_partner
    app.register_blueprint(find_partner.bp)
    
    from . import profile
    app.register_blueprint(profile.bp)

    return app