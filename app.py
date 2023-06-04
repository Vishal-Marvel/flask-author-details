from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Sample data for authors
authors = [
    {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
    {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
]

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Add your authentication logic here
        # For simplicity, let's assume authentication is successful
        session['username'] = username
        return redirect('/author-details')
    
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

# Author details entry route
@app.route('/author-details', methods=['GET', 'POST'])
def author_details():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        # Add your database insertion logic here
        
        return redirect('/author-details')

    return render_template('author_details.html')

# Details search route
@app.route('/details-search', methods=['GET', 'POST'])
def details_search():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        search_term = request.form['search_term']
        
        # Add your database search logic here
        # For simplicity, let's assume the search returns a list of authors
        search_results = [author for author in authors if search_term.lower() in author['name'].lower()]
        
        return render_template('details_search.html', search_results=search_results)

    return render_template('details_search.html')


if __name__ == '__main__':
    app.run(debug=True)
