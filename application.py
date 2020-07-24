import os
import requests
import urllib.parse

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime

from helpers import apology, login_required, global_options, load_page, global_menu, admin_default_tags


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static/uploads")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database

# pythonanywhere connection
# db = SQL('sqlite:///%s/mysite/cms.db' % os.getcwd())

# local and heroku
db = SQL('sqlite:///%s/cms.db' % os.getcwd())


@app.route("/")
def index():

    # load global options
    opt = global_options(db)
    menu = global_menu(db)

    # load page options
    this_page = load_page(db, "homepage")
    if this_page == False:
        return apology("Sorry, page not found", 404)
    else:
        
        # load all post in Homepage
        sql_main = "SELECT post.idpost, post.url, post.title, post.subtitle, post.photo as photo, post.tags, users.name FROM post, users WHERE post.idusers = users.id AND post.is_visible=1 AND post.idpost_place=1 ORDER BY date DESC LIMIT 0,1;"
        sql_main_others = "SELECT post.*, users.name FROM post, users WHERE post.idusers = users.id AND post.is_visible=1 AND post.idpost_place=1 ORDER BY date DESC LIMIT 1,9;"
        sql_aside = "SELECT post.*, users.name FROM post, users WHERE post.idusers = users.id AND post.is_visible=1 AND post.idpost_place=2 ORDER BY date DESC LIMIT 3;"

        main = db.execute(sql_main)
        aside = db.execute(sql_aside)
        main_others = db.execute(sql_main_others)

        return render_template("base.html", opt = opt, page = this_page, menu = menu, post_main = main, post_aside = aside, post_main_others = main_others)


@app.route('/pages/homepage')
def page_url_homepage():
    return redirect("/")


@app.route('/pages/<page_url>')
def page_url(page_url):

    # load global options
    opt = global_options(db)
    menu = global_menu(db)

    # load page options
    this_page = load_page(db, page_url)
    if this_page == False:
        return apology("Sorry, page not found", 404)
    else:
        print(f"homepage: {this_page}")
        return render_template("base_page.html", opt = opt, page = this_page, menu = menu)


@app.route('/post/<post_url>')
def post_url(post_url):

    # load global options
    opt = global_options(db)
    menu = global_menu(db)
    
    # load post 
    post = db.execute("SELECT post.*, users.photo as user_photo, users.name FROM post, users WHERE post.idusers = users.id AND url = :url AND is_visible=1",
                    url = post_url)
    if len(post) == 0:
        return apology("Post not found", 404)
    else:
        datetime_str = str(post[0]['date'])
        datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        date_label = datetime_object.strftime("%A, %B %d, %Y")
        post[0]['date_label'] = date_label


    return render_template("base_post.html", opt = opt, page = post[0], menu = menu)






##############################################################################################################
##############################################################################################################
# ADMIN ROUTES
##############################################################################################################





@app.route("/admin", methods=["GET", "POST"])
def admin():
    if 'user_id' in session:
        # there is a valid session, redirect to admin/home
        return redirect("/admin/home")
    else:

        # load page LOGIN metadata from db.pages
        this_page = load_page(db, "login")

        # load global options
        opt = global_options(db)
        menu = global_menu(db)

        return render_template("admin-login.html", opt = opt, page = this_page, menu = menu)


@app.route("/admin/home", methods=["GET", "POST"])
@login_required
def admin_home():

    # load global options
    opt = global_options(db)
    menu = global_menu(db)

    this_page = admin_default_tags()

    # load online posts in admin/home    
    if session['user_level'] < 3:
        sql = "SELECT post.*, users.name FROM post, users WHERE post.idusers = users.id AND post.is_visible=1 ORDER BY post.date DESC LIMIT 20"
        rows = db.execute(sql)
    else:
        sql = "SELECT post.*, users.name FROM post, users WHERE post.idusers = users.id AND post.is_visible=1 AND post.idusers=:id_linked_user ORDER BY post.date DESC LIMIT 20"
        rows = db.execute(sql,
                        id_linked_user = session['user_id'])    

    return render_template("admin-home.html", opt = opt, menu = menu, page = this_page, rows = rows)


@app.route("/admin/drafts", methods=["GET", "POST"])
@login_required
def admin_drafts():

    # load global options
    opt = global_options(db)
    menu = global_menu(db)

    this_page = admin_default_tags()

    # load online posts in admin/home    
    if session['user_level'] < 3:
        sql = "SELECT post.*, users.name FROM post, users WHERE post.idusers = users.id AND post.is_visible=0 ORDER BY post.date DESC LIMIT 20"
        rows = db.execute(sql)
    else:
        sql = "SELECT post.*, users.name FROM post, users WHERE post.idusers = users.id AND post.is_visible=0 AND post.idusers=:id_linked_user ORDER BY post.date DESC LIMIT 20"
        rows = db.execute(sql,
                        id_linked_user = session['user_id'])

    return render_template("admin-drafts.html", opt = opt, menu = menu, page = this_page, rows = rows)



# /admin/post/create
@app.route("/admin/post/create", methods=["GET", "POST"])
@login_required
def admin_post_create():

    rows = db.execute("INSERT INTO post (is_visible, title, text, idusers, idpost_place) VALUES (0, 'new post', '', :idusers, 0)",
                        idusers = session["user_id"])

    print(f"rows: {rows}")

    url = "/admin/post/" + str(rows)
    return redirect(url)



@app.route("/admin/post/delete", methods=["GET", "POST"])
@login_required
def admin_post_delete():

    if request.method == "GET":

        if not request.args.get("id"):
            return apology("must provide idpost to delete", 403)

        post_id = request.args.get("id")
        # security control
        if session['user_level'] == 3:

            sql = "SELECT * FROM post WHERE idpost = :idpost AND idusers = :id"
            post = db.execute(sql,
                        idpost = post_id, id = session['user_id'])

            if len(post) == 0:
                # not allowed
                return apology("Not allowed to delete this post", 301)
            
            print(f"Post cancellato da utente livello 3")
            return redirect("/admin/home")

        # now I can delete safely the post
        post_delete = db.execute("DELETE FROM post WHERE idpost = :idpost",
                        idpost = post_id)

        print(f"Post cancellato da utente livello <> 3")
        return redirect("/admin/home")



    else:
        return apology("Cannot delete via POST", 501)



@app.route("/admin/post_content/<id>", methods=["GET", "POST"])
@login_required
def admin_post_content(id):

    sql = "SELECT text FROM post WHERE idpost = :idpost "
    content = db.execute(sql, 
            idpost = id)
    
    print(f"content: {content}")

    if len(content) > 0:
        return {
            "html": content[0]['text'],
            "status": 200
        }
    else:
        return { "status": 500}

@app.route("/admin/post_save", methods=["GET", "POST"])
@login_required
def admin_post_save():

    if request.method == "POST":

        valid = 1
        description = ""

        #for k, v in request.form.items():
            #print(k, v)

        #for k, v in request.files.items():
            #print(k, v)
        
        post_id = request.form.get("idpost")

        text_html = request.form.get("editor_html")

        title = request.form.get("title")
        if len(title) == 0:
            valid = 0
            description = "Title cannot be empty"
                
        # check if this user can update this post
        if session['user_level'] == 3:

            sql = "SELECT * FROM post WHERE idpost = :idpost AND idusers = :id"
            post = db.execute(sql,
                        idpost = post_id, id = session['user_id'])

            if len(post) == 0:
                # not allowed
                return apology("Not allowed to delete this post", 301)


        # other levels are allowed
        sql = "UPDATE post SET title=:title, is_visible=:is_visible, meta_title = :meta_title, meta_description = :meta_description, "
        sql = sql + " meta_keywords = :meta_keywords "
        sql = sql + " ,text = :text "
        sql = sql + " ,subtitle = :subtitle "
        sql = sql + " ,tags = :tags "
        sql = sql + " ,idpost_place = :idpost_place "
        
        if request.form.get("url"):
            url = urllib.parse.quote(request.form.get("url"))
            sql = sql + " ,url = '" + url + "' "


        # check if the post request has the file part
        if 'pic' in request.files:
            
            pic = request.files['pic']
        
            if pic.filename != '':
                
                filename = secure_filename(pic.filename)
                pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                sql = sql + " ,photo = '" + filename + "' "

        

        

        sql = sql + " WHERE idpost = :idpost"
               
        updatePost = db.execute(sql, 
                    idpost = post_id, title = title, is_visible = request.form.get("is_visible"), meta_title = request.form.get("meta_title"), 
                    meta_description = request.form.get("meta_description"), meta_keywords = request.form.get("meta_keywords"), text = text_html,
                    tags = request.form.get("tags"), subtitle = request.form.get("subtitle"), idpost_place = request.form.get("idpost_place"))

        # print(f"updatePost: {updatePost}")

        return redirect(request.referrer)


    return apology("wait", 500)


# /admin/post/[id]
@app.route("/admin/post/<post_id>", methods=["GET", "POST"])
@login_required
def admin_post_mod(post_id):

    print(f"post_id:{post_id}")
    # load global options
    opt = global_options(db)
    menu = global_menu(db)
    this_page = admin_default_tags()

    # load single post and load template
    print(f"user_id {session['user_id']}")
    print(f"user_level {session['user_level']}")

    if session['user_level'] <= 2:
        sql = "SELECT * FROM post WHERE idpost = :idpost"
        post = db.execute(sql,
                    idpost = post_id)
    else:
        sql = "SELECT * FROM post WHERE idpost = :idpost AND idusers = :id"
        post = db.execute(sql,
                    idpost = post_id, id = session['user_id'])


    print(f"loaded post: {post}")

    return render_template("admin-post-modify.html", opt = opt, menu = menu, page = this_page, post = post)








# PAGES ********************
@app.route("/admin/pages", methods=["GET", "POST"])
@login_required
def admin_pages():

    # SECURITY USER LEVEL CHECK
    if session["user_level"] != 1:
        return redirect("/admin/home")


    # load global options
    opt = global_options(db)
    menu = global_menu(db)
    this_page = admin_default_tags()

    # load online posts in admin/home
    rows = db.execute("SELECT * FROM pages ORDER BY locked DESC, menu_item DESC, is_visible DESC")

    return render_template("admin-pages.html", opt = opt, menu = menu, page = this_page, rows = rows)



# /admin/page/[id]
@app.route("/admin/pages/<page_id>", methods=["GET", "POST"])
@login_required
def admin_page_mod(page_id):

    # SECURITY USER LEVEL CHECK
    if session["user_level"] != 1:
        return redirect("/admin/home")
    

    # load global options
    opt = global_options(db)
    menu = global_menu(db)
    this_page = admin_default_tags()

    # load single post and load template
    if session['user_level'] == 1:
        sql = "SELECT * FROM pages WHERE idpages = :idpages"
        post = db.execute(sql,
                    idpages = page_id)
    else:
        return apology("Sorry, you're not authorized to manage pages", 301)

    return render_template("admin-page-modify.html", opt = opt, menu = menu, page = this_page, post = post)


@app.route("/admin/page_save", methods=["GET", "POST"])
@login_required
def admin_page_save():

    # SECURITY USER LEVEL CHECK
    if session["user_level"] != 1:
        return redirect("/admin/home")

    if request.method == "POST":

        # check if this user can update this post
        if session['user_level'] > 1:

            return apology("Not allowed to manage this page", 301)

        valid = 1
        description = ""

        page_locked = int(request.form.get("page_locked"))
        page_id = request.form.get("idpages")

        text_html = request.form.get("editor_html")

        if page_locked == 0:

            title = request.form.get("title")
            if len(title) == 0:
                valid = 0
                description = "Title cannot be empty"
                
            # other levels are allowed
            sql = "UPDATE pages SET title=:title, is_visible=:is_visible, meta_title = :meta_title, meta_description = :meta_description, "
            sql = sql + " meta_keywords = :meta_keywords, menu_item = :menu_item "
            sql = sql + " ,text = :text "
            sql = sql + " ,subtitle = :subtitle "  
            
            if request.form.get("url"):
                url = urllib.parse.quote(request.form.get("url"))
                sql = sql + " ,url = '" + url + "' "

            # check if the post request has the file part
            if 'pic' in request.files:
                
                pic = request.files['pic']
            
                if pic.filename != '':
                    
                    filename = secure_filename(pic.filename)
                    pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    
                    sql = sql + " ,photo = '" + filename + "' "

            sql = sql + " WHERE idpages = :idpages"
                
            updatePost = db.execute(sql, 
                        idpages = page_id, title = title, is_visible = request.form.get("is_visible"), meta_title = request.form.get("meta_title"), 
                        meta_description = request.form.get("meta_description"), meta_keywords = request.form.get("meta_keywords"), text = text_html,
                        subtitle = request.form.get("subtitle"), menu_item = request.form.get("menu_item"))

            return redirect(request.referrer)

        else:

            # locked_page == 1 => pagina bloccata

            # other levels are allowed
            sql = "UPDATE pages SET meta_title = :meta_title, meta_description = :meta_description, "
            sql = sql + " meta_keywords = :meta_keywords "
            sql = sql + " ,text = :text "
        
            # check if the post request has the file part
            if 'pic' in request.files:
                
                pic = request.files['pic']
            
                if pic.filename != '':
                    
                    filename = secure_filename(pic.filename)
                    pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    
                    sql = sql + " ,photo = '" + filename + "' "

            sql = sql + " WHERE idpages = :idpages"
        
            updatePost = db.execute(sql, 
                        idpages = page_id, meta_title = request.form.get("meta_title"), 
                        meta_description = request.form.get("meta_description"), meta_keywords = request.form.get("meta_keywords"), text = text_html)

            return redirect(request.referrer)
            


    return apology("wait", 500)


@app.route("/admin/page_content/<id>", methods=["GET", "POST"])
@login_required
def admin_page_content(id):

    # SECURITY USER LEVEL CHECK
    if session["user_level"] != 1:
        return redirect("/admin/home")

    sql = "SELECT text FROM pages WHERE idpages = :idpages "
    content = db.execute(sql, 
            idpages = id)
    
    #print(f"content: {content}")

    if len(content) > 0:
        return {
            "html": content[0]['text'],
            "status": 200
        }
    else:
        return { "status": 500}


# /admin/page/create
@app.route("/admin/pages/create", methods=["GET", "POST"])
@login_required
def admin_pages_create():

    rows = db.execute("INSERT INTO pages (is_visible, title, text) VALUES (0, 'new page', '<p>page content</p>')")

    url = "/admin/pages/" + str(rows)
    return redirect(url)

# /admin/page/delete
@app.route("/admin/pages/delete", methods=["GET", "POST"])
@login_required
def admin_pages_delete():

    if session['user_level'] != 1:
        return apology("You are not authorized to access this functionality", 301)
    
    # check if page is not locked and not deletable
    idpages = request.args.get("id")
    if len(idpages) == 0:
        return apology("Page not recognized", 303)

    check = db.execute("SELECT idpages FROM pages WHERE idpages=:idpages AND locked=0",
                        idpages = idpages)
    
    if len(check) == 0:
        return apology("This page cannot be deleted", 302)
    
    # delete page
    delete = db.execute("DELETE FROM pages WHERE idpages=:idpages AND locked=0",
                        idpages = idpages)
    
    return redirect("/admin/pages")




################### USERS

@app.route("/admin/users", methods=["GET", "POST"])
@login_required
def admin_users():

    # load global options
    opt = global_options(db)
    menu = global_menu(db)

    this_page = admin_default_tags()

    # load online posts in admin/home
    rows = db.execute("SELECT users.*, users_level.* FROM users, users_level WHERE users.idusers_level = users_level.idusers_level ORDER BY users.idusers_level ASC, users.email ASC")

    return render_template("admin-users.html", opt = opt, menu = menu, page = this_page, rows = rows)


# /admin/users/create
@app.route("/admin/users/create", methods=["GET", "POST"])
@login_required
def admin_users_create():

    today = datetime.today()
    
    rows = db.execute("INSERT INTO users (active, email, name, idusers_level, password ) VALUES (0, '', 'new user', 3, :hps)",
                    hps = generate_password_hash(str(today)))

    url = "/admin/users/" + str(rows)
    return redirect(url)


# /admin/users/delete
@app.route("/admin/users/delete", methods=["GET", "POST"])
@login_required
def admin_users_delete():

    iduser = request.args.get("id")
    # to delete a user I must verify if has some post on blog
    check = db.execute("SELECT count(idpost) as tot FROM post WHERE idusers=:idusers",
                        idusers = iduser)

    print(f"check: {check}")   
    if check[0]['tot'] > 0:
        return apology("This user has some post in blog, cannot proceed to delete him", 500)

    # this user can be deleted
    delele = db.execute("DELETE FROM users WHERE id=:idusers",
                        idusers = iduser)
    
    return redirect("/admin/users")




# /admin/users/save
@app.route("/admin/users/save", methods=["GET", "POST"])
@login_required
def admin_users_save():

    idusers = request.form.get("idusers")
    user_level = request.form.get("user_level")
    active = request.form.get("active")
    name = request.form.get("name")
    if len(name) == 0:
        return apology("Name value is not valid", 500)
    
    email = request.form.get("email")
    if len(email) == 0:
        return apology("E-mail value is not valid", 500)
    
    password = request.form.get("password")
    if len(password) == 0:
        sql = "UPDATE users SET active = :active, idusers_level = :user_level, name = :name, email = :email " 
        sql = sql + " WHERE id = :id"
        updatePost = db.execute(sql, 
                id = idusers, name = name, email = email, user_level = user_level, active = active)

    else:
        sql = "UPDATE users SET active = :active, idusers_level = :user_level, name = :name, email = :email, password = :password " 
        sql = sql + " WHERE id = :id"
        updatePost = db.execute(sql, 
                id = idusers, name = name, email = email, password = generate_password_hash(password), user_level = user_level, active = active)

    return redirect("/admin/users")




@app.route("/admin/users/<id>", methods=["GET", "POST"])
@login_required
def admin_users_detail(id):

    opt = global_options(db)
    menu = global_menu(db)
    this_page = admin_default_tags()

    sql = "SELECT * FROM users WHERE id = :id "
    content = db.execute(sql, 
            id = id)
    
    if len(content) == 0:
        return apology("User not found", 500)
    
    # load user levels
    user_level = db.execute("SELECT * FROM users_level ORDER BY idusers_level ASC")

    return render_template("admin-users-detail.html", profile = content[0], user_level = user_level, opt = opt, menu = menu, page = this_page)
    

################### PROFILE

@app.route("/admin/profile", methods=["GET", "POST"])
@login_required
def admin_profile():

    # load global options
    opt = global_options(db)
    menu = global_menu(db)
    this_page = admin_default_tags()

    profile = db.execute("SELECT * FROM users WHERE id = :id",
                    id = session["user_id"])

    if len(profile) == 0:
        return apology("I can't find your user profile in database",500)
    else:
        return render_template("admin-profile.html", profile = profile[0], opt = opt, menu = menu, page = this_page)


@app.route("/admin/profile_save", methods=["GET", "POST"])
@login_required
def admin_profile_save():

    if request.method == "POST":

        valid = 1
        description = ""
        sql = ""
        sql_photo = ""

        name = request.form.get("name")
        if len(name) == 0:
            return apology("Name cannot be empty", 500)
        
        email = request.form.get("email")
        if len(email) == 0:
            return apology("E-Mail cannot be empty", 500)

        # check if the post request has the file part
        if 'pic' in request.files:
            
            pic = request.files['pic']
        
            if pic.filename != '':
                
                filename = secure_filename(pic.filename)
                pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                sql_photo = " ,photo = '" + filename + "' "
                print(f"sql_photo: {sql_photo}")
        
        password = request.form.get("password")
        if len(password) == 0:
            sql = "UPDATE users SET name = :name, email = :email " + sql_photo
            sql = sql + " WHERE id = :id"
            updatePost = db.execute(sql, 
                    id = session["user_id"], name = name, email = email)

        else:
            sql = "UPDATE users SET name = :name, email = :email, password = :password " + sql_photo
            sql = sql + " WHERE id = :id"
            updatePost = db.execute(sql, 
                    id = session["user_id"], name = name, email = email, password = generate_password_hash(password))

        # go back to profile page, everything should be ok
        return redirect(request.referrer)

    return apology("wait", 500)

















@app.route("/admin/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE active=1 AND email = :email",
                          email=request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            print("No user valid")
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_name"] = rows[0]["name"]
        session["user_level"] = rows[0]["idusers_level"]

        # Redirect user to home page
        return redirect("/admin/home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return redirect("/admin")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")





def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
