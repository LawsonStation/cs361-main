import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_random_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'  # SQLite for simplicity
    SQLALCHEMY_TRACK_MODIFICATIONS = False
