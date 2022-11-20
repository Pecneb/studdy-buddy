from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from studdybuddy.auth import login_required

bp = Blueprint('menu', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('menu/index.html')