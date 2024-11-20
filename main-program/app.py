from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import config
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import base64
# from app\models import db, Item, User
# from models import Junkyard, item_test


app = Flask(__name__, template_folder='app/static/templates', static_folder='app/static')
app.secret_key = 'capybara'  # Secret key for session management.

# Database helper function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Enable named columns
    return conn

# Initialize SQLite Database tables
connect = sqlite3.connect('database.db') 
connect.execute( 
    'CREATE TABLE IF NOT EXISTS PARTICIPANTS ( \
         name TEXT, \
         email TEXT, \
         city TEXT, \
         country TEXT, \
         phone TEXT)'
         ) 

# connect.execute('DROP TABLE items')
connect.execute(
    'CREATE TABLE IF NOT EXISTS items ( \
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        title TEXT, \
        price FLOAT, \
        description TEXT, \
        city TEXT, \
        state TEXT, \
        zip_code TEXT, \
        photo BLOB)'
    )

# Users
connect.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    email TEXT UNIQUE,
                    password TEXT)''')
connect.close()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to 'login' page for unauthorized users

# Define user_loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return User(user['id'], user['username'], user['email'], user['password']) if user else None


# Routes
@app.route('/')
def landing():
    # return render_template('index.html')
    return render_template('landing.html')

# Database testing
@app.route('/index')
def index():
    return render_template('index.html')
    # return render_template('landing.html')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/join', methods=['GET', 'POST']) 
def join(): 
    if request.method == 'POST': 
        name = request.form['name'] 
        email = request.form['email'] 
        city = request.form['city'] 
        country = request.form['country'] 
        phone = request.form['phone'] 
  
        with sqlite3.connect("database.db") as users: 
            cursor = users.cursor() 
            cursor.execute("INSERT INTO PARTICIPANTS (name,email,city,country,phone) VALUES (?,?,?,?,?)", 
                           (name, email, city, country, phone)) 
            users.commit() 
        return render_template("index.html") 
    else: 
        return render_template('join.html') 
  
  
@app.route('/participants') 
def participants(): 
    connect = sqlite3.connect('database.db') 
    cursor = connect.cursor() 
    cursor.execute('SELECT * FROM PARTICIPANTS') 
  
    data = cursor.fetchall() 
    return render_template("participants.html", data=data) 

# Search route
# @app.route('/search')
# def search():
#     return render_template('search.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')  # Get the search query from the URL parameters
    if query:
        conn = get_db_connection()  # Use the function that sets the row factory
        cursor = conn.cursor()
        
        # Use a SQL query to search by title, description, or any other relevant columns
        cursor.execute("SELECT * FROM items WHERE title LIKE ? OR description LIKE ?", ('%' + query + '%', '%' + query + '%'))
        
        data = cursor.fetchall()
        conn.close()
    # Empty query, show search UI
    else:
        data = []
        query = None
        return render_template('search.html')

    return render_template("search_results.html", data=data, query=query)


@app.route('/create_listing', methods=['GET', 'POST'])
def create_listing():
    if request.method == 'POST':
        title = request.form['title']
        # currency = request.form['currency']
        price = request.form['price']
        description = request.form['description']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']

        photo = request.files['photo']
        # Read the photo data and encode.
        photo_data = base64.b64encode(photo.read()).decode('utf-8') if photo else None


        with sqlite3.connect("database.db") as items:
            cursor = items.cursor()
            cursor.execute(
                '''
                INSERT INTO items (title, price, description, city, state, zip_code, photo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (title, price, description, city, state, zip_code, photo_data)
            )
            items.commit()
        return redirect(url_for('browse'))
    else:
        return render_template('create_listing.html')
    
@app.route('/confirm_cancel')
def confirm_cancel():
    return render_template('confirm_cancel.html')

@app.route('/cancel')
def cancel():
    return redirect(url_for('home')) 


@app.route('/browse')
def browse():
    # connect = sqlite3.connect('database.db')
    connect = get_db_connection()
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM items')

    data = cursor.fetchall()
    return render_template('browse.html', data=data)

@app.route('/messages')
def messages():
    return render_template('messages.html')

@app.route('/account')
def account():
    return render_template('account.html')

# sqlite connector
# @app.route('/items')
# def items():
#     connect = sqlite3.connect('database.db')
#     cursor = connect.cursor()
#     cursor.execute('SELECT * FROM items WHERE id = ?', (item_id))

#     data = cursor.fetchone()
#     return render_template('item_detail.html', item=item)
    
@app.route('/item/<int:item_id>')
def item_detail(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch the item with the specified ID
    cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
    item = cursor.fetchone()  # This will now be a Row object

    conn.close()

    # Check if the item was found
    if item is None:
        return "Item not found", 404  # Return 404 if item not found

    return render_template('item_detail.html', item=item)  # Pass the Row object to the template

@app.route('/delete_listing/<int:item_id>', methods=['POST'])
def delete_listing(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Delete the item with the specified ID
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    
    flash("Listing deleted successfully.", "info")
    return redirect(url_for('browse'))


# @app.route('/items')
# def items():
#     connect =sqlite3.connect('database.db')
#     cursor = connect.cursor()
#     cursor.execute('SELECT * FROM items')

#     data = cursor.fetchall()
#     return render_template("browse.html", data=data)



# User class
class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

# Registration and login routes.
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (username, email, hashed_password))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists.', 'error')
            return redirect(url_for('register'))
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data['id'], user_data['username'], user_data['email'], user_data['password'])
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))  # Route after login
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Login protected routes
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)


if __name__ == '__main__':
    app.run(debug=True)