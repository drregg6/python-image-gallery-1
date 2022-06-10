from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return """
<!DOCTYPE html>
<html>
   <head>
      <title>Hello</title>
      <meta charset="utf-8" />
   </head>
   <body>
     <a href="/admin">Proceed as admin</a>
   </body>
</html>
"""
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
