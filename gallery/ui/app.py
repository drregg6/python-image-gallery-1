from flask import Flask, request, render_template, redirect, session, flash
from gallery.data.db import connect
from gallery.data.postgres_user_dao import PostgresUserDAO
from gallery.data.secrets import get_secret_flask_session
from functools import wraps

app = Flask(__name__)
app.secret_key = get_secret_flask_session()
connect()

def postgres_user_dao():
    return PostgresUserDAO()

def check_admin():
    return 'username' in session and session['username'] == 'fred'

def check_user():
    # this should check for username AND if session[username] is the same as the image_gallery
    return 'username' in session

def requires_user(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_user():
            return redirect('/')
        return view(**kwargs)
    return decorated

def requires_admin(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_admin():
            return redirect('/login')
        return view(**kwargs)
    return decorated

############################
######### HOME #############
############################

@app.route('/')
def home():
    return render_template('index.html')

#############################
####### ADMIN ROUTES ########
#############################

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = postgres_user_dao().get_user(request.form['username'])
        if user is None or user.password != request.form['password']:
            flash('Username / password combo incorrect')
            return redirect('/login/')
        else:
            flash('Successfully logged in - welcome!')
            session['username'] = request.form['username']
            return redirect('/')
    else:
        return render_template('login.html')

@app.route('/debugSession/')
def debug_session():
    result = ""
    for key,value in session.items():
        result += key + "=>" + str(value) + "<br />"
    return result

@app.route('/admin/users/')
@requires_admin
def admin():
    return render_template('admin.html', users=postgres_user_dao().get_users())

@app.route('/admin/users/<string:username>/')
@requires_admin
def get_user(username):
    return render_template('user.html', user=postgres_user_dao().get_user(username))

@app.route('/admin/create-user/', methods = ['GET', 'POST'])
@requires_admin
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        postgres_user_dao().create_user(username, password, full_name)
        flash('User ' + username + ' created')
        return redirect('/admin/users')
    else:
        return render_template('create_user.html')

@app.route('/admin/modified-user/', methods = ['POST'])
def modified_user():
    print(request.form)
    username = request.form['username']
    password = request.form['password']
    full_name = request.form['full_name']
    postgres_user_dao().modify_user(username, password, full_name)
    flash('User ' + username + ' modified')
    return redirect("/admin/users")

@app.route('/admin/delete/<string:username>/')
@requires_admin
def delete_user(username):
    return render_template("confirm.html",
            title="Confirm delete",
            msg="Are you sure you want to delete " + username + "? ",
            on_yes="/admin/execute-delete/" + username + "/",
            on_no="/admin/users/")

@app.route('/admin/execute-delete/<string:username>/')
def execute_delete_user(username):
    postgres_user_dao().delete_user(username)
    flash('User deleted')
    return redirect("/admin/users")

####################################
########### IMAGE ROUTES ###########
####################################

@app.route('/upload-image/', methods = ['GET', 'POST'])
@requires_user
def upload_image():
    if request.method == 'POST':
        image = request.form['image']
        username = session['username']
        # save image in the username bucket
        flash('Image uploaded successfully!')
        return redirect('/upload-image')
    else:
        return render_template('upload_image.html')
#WIP
#@app.route('/view-gallery/')
#@requires_user
# images = [{"name": "image", "src": "http://placehold.it/50x50"}]
#def view_gallery():
#    return render_template('view_gallery.html', images=images)
