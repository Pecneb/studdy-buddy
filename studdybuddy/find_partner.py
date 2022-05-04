from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from studdybuddy.db import get_db
from studdybuddy.auth import login_required

bp = Blueprint('findpartner', __name__, url_prefix='/findpartner')

@bp.route('/')
@login_required
def findpartner():
    return render_template('find_partner/find_partner.html')