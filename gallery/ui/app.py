from flask import Flask
from flask import request
from flask import render_template
from gallery.data.db import connect

app = Flask(__name__)
connect()

@app.route('/')
def home():
    return 'Hello World!'

@app.route('/admin/')
def admin():
    users = [('fred', 'password', 'fred flintstone'), ('barney', 'simple', 'barney rubble'), ('dino', 'dinosaur', 'dino dinosaur')]
    return render_template('admin.html/', users=users)

@app.route('/admin/<string:username>/')
def get_user(username):
    user = ('fred', 'password', 'fred flintstone')
    return render_template('user.html', username=username, user=user)

@app.route('/admin/create-user')
def create_user():
    return render_template('create_user.html')

@app.route('/admin/user-created', methods = ['POST'])
def user_created():
    username = request.form['username']
    password = request.form['password']
    full_name = request.form['full_name']
    return "User " + username + " has been created!"

@app.route('/app/modified-user', methods = ['POST'])
def modified_user():
    username = request.form['username']
    password = request.form['password']
    full_name = request.form['full_name']
    return 'User ' + username + ' has been modified!'

@app.route('/admin/<string:username>/delete')
def delete_user(username):
    return "If you are sure you want to delete the user, <a href="">click here</a>"
