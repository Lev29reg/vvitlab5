import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="2846",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            if username == '':
                return render_template('account.html', nouser=1)
            elif password == '':
                return render_template('account.html', nopass=1)
            elif len(records) < 1:
                return render_template('account.html', unidentified=1)
            else:
                return render_template('account.html', full_name=records[0][1], password=records[0][3],
                                       login=records[0][2])
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()
        if name == "":
            return render_template('account.html', noname=1)
        if login == "":
            return render_template('account.html', nouser=1)
        if password == "":
            return render_template('account.html', nopass=1)
        return redirect('/login/')

    return render_template('registration.html')


