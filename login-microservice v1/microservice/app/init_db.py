from app import create_app
from app.models import db

# Create the app instance
app = create_app()

# Use the app's context to interact with the database
with app.app_context():
    # Create all the tables (based on the models)
    db.create_all()
    print("Database initialized and tables created.")
