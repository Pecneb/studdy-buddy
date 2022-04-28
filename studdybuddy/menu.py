from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from studdybuddy.db import get_db
from studdybuddy.auth import login_required

bp = Blueprint('menu', __name__, url_prefix='/menu')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def menu():
    if request.method == 'POST':
        pass
    render_template('menu/menu.html')