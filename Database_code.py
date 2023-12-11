import sqlite3

# Connect to the database (creates a new database if it doesn't exist)
conn = sqlite3.connect('enemies.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the enemies table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS enemies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        level INTEGER,
        health INTEGER,
        damage_output INTEGER,
        items TEXT,
        armour TEXT,
        sex TEXT,
        personality TEXT
    )
''')

# Insert data into the enemies table
cursor.execute('''
    INSERT INTO enemies (level, health, damage_output, items, armour, sex, personality)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', (1, 100, 50, 'Sword', 'Plate', 'Male', 'Aggressive'))

# Commit the changes and close the connection
conn.commit()
conn.close()

