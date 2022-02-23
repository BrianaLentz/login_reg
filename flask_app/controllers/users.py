from ast import Not
from contextlib import nullcontext
from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.user import User
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def login_reg():
    return render_template('login_reg.html')

    
@app.route('/register', methods=['POST'])
def register():
    if not User.validate_reg(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data ={
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
    }
    id = User.save(data)
    session['id'] = id
    return redirect('/dashboard')


@app.route('/dashboard')
def success():
    if not session:
        return redirect('/')
    return render_template('success.html', user=session)


@app.route('/login', methods=['POST'])
def login():
    data = {'email' : request.form['email']}
    user = User.validate_email(data)
    if not user:
        flash("Email provided not valid", 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Email/Password provided not valid', 'login')
        return redirect('/')
    session['id'] = user.id
    session['first_name'] = user.first_name
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')