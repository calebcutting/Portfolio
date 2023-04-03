import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.sql import exists

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'database.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
class Student(db.Model):
    id = db.Column(db.Integer,unique=True, primary_key=True)
    u_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Student {self.u_name}>'


class comment(db.Model):
    id = db.Column(db.Integer,unique=True, primary_key=True)
    poster = db.Column(db.String(100), nullable=False)
    chat = db.Column(db.String(200), nullable=False)
    def __repr__(self):
        return f'<{self.chat}>'

def get_rows():
    rows = db.query(Student).count()
    return rows


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')

@app.route('/sign_in', methods=['POST'])
def sign_in():
    user_name = request.form['user_name']
    password = request.form['user_password']
    check = db.session.query(exists().where(Student.u_name == user_name, Student.password == password)).scalar()
    if check==True:
        return render_template('home.html', user_using=user_name)
    else:
        return render_template('login.html', warning='User does not exist.')



@app.route('/log_in')
def log_in():
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        confirm_password = request.form['confirm_password']
        user_name = request.form['user_name']
        password = request.form['user_password']


        if confirm_password == password:
            if 100 > len(password) > 7:
                if db.session.query(exists().where(Student.u_name == user_name)).scalar() == False:
                    current_user = Student(u_name=user_name, password=password)
                    print(current_user.u_name)
                    db.session.add(current_user)
                    db.session.commit()
                    return render_template('home.html', user_using=user_name)
                else:
                    return render_template('index.html', warning="That is already a member, please enter a name that is original.")
            elif len(password) < 8:
                return render_template('index.html', warning="That password is too short. ")
            else:
                return render_template('index.html', warning="That password is too long. ")

        return render_template('index.html', warning='Passwords do not match.')
    except:
        return render_template('index.html', warning="Error")

@app.route('/send_chat', methods=['POST'])
def send_chat():
    chat_posted = request.form['chat']
    chat_poster = request.form['poster']
    c1 = comment(poster=chat_poster, chat=chat_posted)
    db.session.add(c1)
    db.session.commit()
    return render_template('home.html', message=c1, user_using=chat_poster)

if __name__ == '__main__':
    db.create_all()
    app.run()
