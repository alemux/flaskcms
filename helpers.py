import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):

        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/admin")
        return f(*args, **kwargs)
    return decorated_function


def global_options(db):

    globals = db.execute("SELECT * FROM options WHERE id=1")
    return globals[0]

def load_page(db, url):

    page = db.execute("SELECT * FROM pages WHERE url = :url AND is_visible=1",
                        url = url)
    print(f"[load_page] page {page}")
    if len(page) == 0:
        return False
    else:
        return page[0]



def global_menu(db):

    menu = db.execute("SELECT url, title FROM pages WHERE is_visible=1 AND menu_item=1 ORDER BY menu_order ASC")
    return menu

def admin_default_tags():
    tags = {
        'meta_title': 'ADMIN CONTROL PANEL'
    }
    return tags