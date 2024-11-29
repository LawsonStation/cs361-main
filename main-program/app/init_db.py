import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')  # database name
    cursor = conn.cursor()

    # Create a test items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items_test (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price FLOAT NOT NULL,
            description TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            zip_code TEXT NOT NULL
        )            
    ''')

    # # Create the users table
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS users (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         username TEXT NOT NULL UNIQUE,
    #         email TEXT NOT NULL UNIQUE,
    #         password TEXT NOT NULL,  -- Store hashed passwords in production
    #         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #     )
    # ''')

    # # Create the categories table
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS categories (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         name TEXT NOT NULL UNIQUE,
    #         description TEXT
    #     )
    # ''')

    # # Create the listings table
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS listings (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         title TEXT NOT NULL,
    #         currency TEXT NOT NULL,
    #         description TEXT NOT NULL,
    #         location_city TEXT NOT NULL,
    #         location_state TEXT NOT NULL,
    #         location_country TEXT NOT NULL,
    #         location_zip TEXT NOT NULL,
    #         posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    #         posted_by INTEGER NOT NULL,  -- Foreign key referencing users
    #         price REAL NOT NULL,
    #         category_id INTEGER,  -- Foreign key referencing categories
    #         FOREIGN KEY (posted_by) REFERENCES users (id),
    #         FOREIGN KEY (category_id) REFERENCES categories (id)
    #     )
    # ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
