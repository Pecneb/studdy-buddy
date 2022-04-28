from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for
        )

from werkzeug.exceptions import abort

from studdybuddy.auth import login_required, load_logged_in_user
from studdybuddy.db import get_db

bp = Blueprint('user', __name__, url_prefix='user')

@bp.route('/profile', methods=('GET', 'POST'))
@login_required
def user_profile():
        if request.method == 'POST':
                pass
        
        return render_template('user/user_profile.html')