import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # SQLite database file
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable track modifications for performance
