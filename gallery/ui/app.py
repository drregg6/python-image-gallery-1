from flask import Flask, request, render_template, redirect, session, flash
from gallery.data.db import connect
from gallery.data.postgres_user_dao import PostgresUserDAO
from gallery.data.postgres_image_dao import PostgresImageDAO
from gallery.data.secrets import get_secret_flask_session
from functools import wraps

app = Flask(__name__)
app.secret_key = get_secret_flask_session()
connect()

print('in app')

##############################
######### HELPERS ############
##############################
def postgres_user_dao():
    return PostgresUserDAO()

def postgres_image_dao():
    return PostgresImageDAO()

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
    if 'username' in session:
        username = session['username']
    else:
        username = None
    return render_template('index.html', username=username)

#############################
######## AUTH ROUTES ########
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

@app.route('/logout/')
def logout():
    if 'username' in session:
        session.pop('username')
        flash('Logout successful')
        return redirect('/')
    else:
        flash('Cannot locate user')
        return redirect('/')

@app.route('/debugSession/')
def debug_session():
    result = ""
    for key,value in session.items():
        result += key + "=>" + str(value) + "<br />"
    return result

#############################
####### ADMIN ROUTES ########
#############################

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
    print('hit route')
    if request.method == 'POST':
        # get vars
        image = request.files['image']
        username = session['username']
        if image.filename == '':
            flash('Please upload an image')
            return redirect('/upload-image')
        print(image)
        print(image.filename)
        # save image in the username bucket
        path = username + "/" + image.filename
        postgres_image_dao().add_image(username, image, path)

        # redirect
        flash('Image uploaded successfully!')
        return redirect('/upload-image/')
    else:
        return render_template('upload_image.html')

@app.route('/view-gallery/<string:username>/')
@requires_user
def view_gallery(username):
    # get user images
    return render_template('view_gallery.html', username=username, images=postgres_image_dao().get_images(username))

@app.route('/view-gallery/<string:username>/<string:image>/')
@requires_user
def view_image(username, image):
    return render_template('view_image.html', image=postgres_image_dao().get_image(username, image))

@app.route('/delete-image/<string:image>/')
@requires_user
def delete_image(image):
        username = session['username']
        image_obj = postgres_image_dao().get_image(username, image)
        return render_template("confirm.html",
            title="Confirm delete",
            msg="Are you sure you want to delete " + image_obj.image_name + "? ",
            on_yes="/delete-image/execute-delete/" + image_obj.image_name + "/",
            on_no="/admin/users/")

@app.route('/delete-image/execute-delete/<string:image>/')
def execute_delete_image(image):
    username = session['username']
    image_obj = postgres_image_dao().get_image(username, image)
    print(repr(image_obj))
    postgres_image_dao().delete_image(image_obj)
    flash('Image deleted')
    return redirect('/')
