from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# SQLAlchemy configurations
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://your_username:your_databse_password@localhost/your_database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# Author model
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_no = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    linkedin = db.Column(db.String(100), nullable=False)
    google_plus = db.Column(db.String(100), nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Perform login authentication
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['username'] = user.username
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Insert new user into the database
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        session['username'] = username
        return redirect('/author-details')

    return render_template('register.html')

# Author details entry route
@app.route('/author-details', methods=['GET', 'POST'])
def author_details():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        contact_no = request.form['contact_no']
        address = request.form['address']
        linkedin = request.form['linkedin']
        google_plus = request.form['google_plus']
        
        # Insert new author details into the database
        new_author = Author(name=name, contact_no=contact_no, address=address, linkedin=linkedin, google_plus=google_plus)
        db.session.add(new_author)
        db.session.commit()

        return redirect('/author-details')

    return render_template('author_details.html')

# Details search route
@app.route('/details-search', methods=['GET', 'POST'])
def details_search():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        search_term = request.form['search_term']
        
        # Search for authors in the database
        search_results = Author.query.filter(Author.name.like('%' + search_term + '%')).all()
        
        return render_template('details_search.html', search_results=search_results)
    
    return render_template('details_search.html')


if __name__ == '__main__':
    app.run(debug=True)