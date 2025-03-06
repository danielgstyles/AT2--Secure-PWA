import bcrypt
import sqlite3

# Step 1: Install the necessary libraries if they are not already installed
# You can install them using pip:
# pip install bcrypt sqlite3

# Step 2: Connect to your SQL database. Here we use SQLite, but you can change it to MySQL, PostgreSQL, etc.
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Step 3: Create a table to store user information (if not already created)
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash BLOB NOT NULL)''')

# Function to create a new user
def create_user(username, password):
    # Hash the password using bcrypt
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Insert the username and hashed password into the database
    cursor.execute('''INSERT INTO users (username, password_hash) VALUES (?, ?)''', 
                  (username, password_hash))
    conn.commit()
    print(f"User {username} created successfully.")

# Function to check a user's login credentials
def check_user(username, password):
    # Retrieve the hashed password from the database
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    
    if result:
        # Compare the hashed password with the provided password
        if bcrypt.checkpw(password.encode('utf-8'), result[0]):
            print(f"Login successful for user {username}.")
            return True
        else:
            print("Incorrect password.")
            return False
    else:
        print("User not found.")
        return False

# Example usage:
create_user('john_doe', 'securepassword123')

# Check login credentials
check_user('john_doe', 'securepassword123')  # Should return True
check_user('john_doe', 'wrongpassword')      # Should return False
