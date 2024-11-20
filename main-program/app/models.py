from flask_sqlalchemy import SQLAlchemy
import sqlite3

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), unique=True, nullable=False)
#     email = db.Column(db.String(150), unique=True, nullable=False)
#     password = db.Column(db.String(150), nullable=False)

#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}')"

# Database helper function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# Model for Item
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True, nullable=False)
    # currency = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    photo = db.Column(db.Blob), nullable=True)

    def __repr__(self):
        return f"ItemTest('{self.title}', '{self.price}', '{self.description}', '{self.city}', '{self.state}', '{self.zip_code}', '{self.photo}')"


# Model for User (Flask-Login) - methods for managing user authentication state.
# class User(UserMixin):
#     def __init__(self, id, username, email, password_hash):
#         self.id = id
#         self.username = username
#         self.email = email
#         self.password_hash = password_hash

#     @staticmethod
#     def get_user_by_id(user_id):
#         conn = get_db_connection()
#         user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
#         conn.close()
#         if user:
#             return User(user['id'], user['username'], user['email'], user['password_hash'])
#         return None

#     @staticmethod
#     def get_user_by_username(username):
#         conn = get_db_connection()
#         user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
#         conn.close()
#         if user:
#             return User(user['id'], user['username'], user['email'], user['password_hash'])
#         return None
