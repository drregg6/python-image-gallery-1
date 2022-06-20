from flask import Flask, request, render_template, redirect
from gallery.data.db import connect
from gallery.data.postgres_user_dao import PostgresUserDAO


app = Flask(__name__)
connect()

def postgres_user_dao():
    return PostgresUserDAO()

@app.route('/')
def home():
    return '<a href="/admin/users">Go to the Admin page</a>'

@app.route('/admin/users/')
def admin():
    return render_template('admin.html', users=postgres_user_dao().get_users())

@app.route('/admin/users/<string:username>/')
def get_user(username):
    return render_template('user.html', user=postgres_user_dao().get_user(username))

@app.route('/admin/create-user/')
def create_user():
    return render_template('create_user.html')

@app.route('/admin/user-created/', methods = ['POST'])
def user_created():
    username = request.form['username']
    password = request.form['password']
    full_name = request.form['full_name']
    postgres_user_dao().create_user(username, password, full_name)
    return redirect("/admin/users")

@app.route('/admin/modified-user/', methods = ['POST'])
def modified_user():
    print(request.form)
    username = request.form['username']
    password = request.form['password']
    full_name = request.form['full_name']
    postgres_user_dao().modify_user(username, password, full_name)
    return redirect("/admin/users")

@app.route('/admin/delete/<string:username>/')
def delete_user(username):
    return render_template("confirm.html",
            title="Confirm delete",
            msg="Are you sure you want to delete " + username + "? ",
            on_yes="/admin/execute-delete/" + username + "/",
            on_no="/admin/users/")

@app.route('/admin/execute-delete/<string:username>/')
def execute_delete_user(username):
    postgres_user_dao().delete_user(username)
    return redirect("/admin/users")
