from flask import Flask, request, redirect, session, flash, render_template
from mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = 'damascusXIII'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def emails():
    emails_db = connectToMySQL('emails').query_db("SELECT id,email,created_at as date FROM emails.user;")
    return render_template('emails.html', emails_tp=emails_db)

@app.route('/process', methods=['POST'])
def validate():
    emails_db = connectToMySQL('emails').query_db("SELECT email FROM emails.user;")

    is_valid = True
    if not EMAIL_REGEX.match(request.form['email']):
        flash('Invalid email address!', 'email')
        is_valid = False
    for email in emails_db:
        if request.form['email'] == email['email']:
            flash('Email is already taken!', 'email')
            is_valid = False
            break

    if not is_valid:
        return redirect('/')
    else:
        data = {
            'email': request.form['email']
        }
        connectToMySQL('emails').query_db('INSERT INTO user(email) VALUES(%(email)s);',data)
        session['new'] = True
        return redirect('/success')

@app.route('/process_delete/<user_id>')
def delete(user_id):
    data = {
        'user_id': user_id
    }
    connectToMySQL('emails').query_db("DELETE FROM user WHERE id=%(user_id)s;", data)
    session['new'] = False
    return redirect('/success')

if __name__ == '__main__':
    app.run(debug=True)