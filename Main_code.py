import random
import time
import sys
import sqlite3
import os
import time

conn = sqlite3.connect('game.db')
c = conn.cursor()

# Create tables if they don't exist

def create_inventory_table():
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 item TEXT,
                 type TEXT,
                 description TEXT,
                 quantity INTEGER,
                 value INTEGER)''')

def add_item_to_inventory(item, item_type, description, quantity, value):
    c.execute("INSERT INTO inventory (item, type, description, quantity, value) VALUES (?, ?, ?, ?, ?)",
              (item, item_type, description, quantity, value))
    conn.commit()

def get_inventory():
    c.execute("SELECT item, description FROM inventory")
    items = c.fetchall()
    if len(items) == 0:
        print("Your inventory is empty.")
    else:
        for item in items:
            print("Your", item[0], "is a/are", item[1])
    return items

def Bag():
    create_inventory_table()
    print("You open your bag:" + "\n")
    items = get_inventory()
    return items


# Room Count
Area_Count = 0

# Enemy Count
Enemy_Count = 0

# Bonuses
def Damage_Bonus():
    global Original_Damage
    Success = random.randint(1,10)
    if Success > 7:
        Original_Damage = character.damage_output
        character.damage_output += 10
        print("You have been granted a bonus. You now deal", character.damage_output ,"damage")

def Health_Bonus():
    global Original_HP
    Success = random.randint(1, 10)
    if Success > 7:
        Original_HP = character.health
        character.health += 10
        print("You have been granted a bonus. Your health is now", character.health)

def Buff_Reset():
    character.damage_output = Original_Damage
    character.health = Original_HP

def Bonus():
    Damage_Bonus()
    Health_Bonus()
    time.sleep(1)

class Enemy_Data():
    def __init__(self, enemy_id, enemy_name, enemy_level, enemy_health, enemy_damage, enemy_items, enemy_armour, enemy_sex, enemy_personality):
        self.enemy_id = enemy_id
        self.enemy_name = enemy_name
        self.enemy_level = enemy_level
        self.enemy_health = enemy_health
        self.enemy_damage = enemy_damage
        self.enemy_items = enemy_items
        self.enemy_armour = enemy_armour
        self.enemy_sex = enemy_sex
        self.enemy_personality = enemy_personality

# Function to generate enemies in the room
def generate_enemies():
    # Check if the database exists
    if os.path.exists('enemies.db'):
        # Retrieve enemies from the database
        enemies = retrieve_enemies()

        # Generate enemies in the room
        if enemies:
            global current_room
            current_room = None  # Define the 'current_room' variable
            if current_room is not None:
                for enemy in enemies:
                    enemy_id, enemy_name, enemy_level, enemy_health, enemy_damage, enemy_items, enemy_armour, enemy_sex, enemy_personality = enemy

                    # Create enemy object and add it to the room
                    enemy_obj = Enemy_Data(enemy_id, enemy_name, enemy_level, enemy_health, enemy_damage, enemy_items, enemy_armour, enemy_sex, enemy_personality)
                    current_room.add_enemy(enemy_obj)
            else:
                print("No current room available.")
        else:
            # Generate random stats for the enemy
            enemy_id = enemy_id + 1
            enemy_name = random.choice(['Goblin', 'Orc', 'Troll', 'Giant', 'Dragon'])
            enemy_level = random.randint(1, 10)
            enemy_health = random.randint(50, 100)
            enemy_damage = random.randint(20, 50)
            enemy_items = random.choice(['Sword', 'Axe', 'Bow', 'Dagger'])
            enemy_armour = random.choice(['Plate', 'Chainmail', 'Leather', 'Cloth'])
            enemy_sex = random.choice(['Male', 'Female'])
            enemy_personality = random.choice(['Aggressive', 'Defensive', 'Passive'])

            # Connect to the database
            conn = sqlite3.connect('enemies.db')
            cursor = conn.cursor()

            # Insert the generated enemy into the enemies table
            cursor.execute('''
                INSERT INTO enemies (level, health, damage_output, items, armour, sex, personality)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (enemy_level, enemy_health, enemy_damage, enemy_items, enemy_armour, enemy_sex, enemy_personality))

            # Commit the changes and close the connection
            conn.commit()
            conn.close()
    else:
        print("Enemies database does not exist.")

# Function to retrieve enemies from the database
def retrieve_enemies():
    # Connect to the database
    conn = sqlite3.connect('enemies.db')
    cursor = conn.cursor()

    # Retrieve enemies from the database
    cursor.execute('SELECT * FROM enemies')
    enemies = cursor.fetchall()

    # Close the connection
    conn.close()

    if not enemies:
        print("No enemies found in the database.")

    global enemy_objects
    global enemy_obj
    enemy_objects = []
    for enemy in enemies:
        enemy_id, enemy_name, enemy_level, enemy_health, enemy_damage, enemy_items, enemy_armour, enemy_sex, enemy_personality = enemy

        # Create enemy object and add it to the list
        enemy_obj = Enemy_Data(enemy_id, enemy_name, enemy_level, enemy_health, enemy_damage, enemy_items, enemy_armour, enemy_sex, enemy_personality)
        enemy_objects.append(enemy_obj)

    return enemy_objects

class Character:
    def __init__(self, name, age, sex, class_type, level, experience=0, health=100, damage_output=10, enemies_killed=0, rooms_completed=0):
        self.name = name
        self.age = age
        self.sex = sex
        self.class_type = class_type
        self.level = level
        self.experience = experience
        self.health = health
        self.damage_output = damage_output
        self.enemies_killed = enemies_killed
        self.rooms_completed = rooms_completed

# Difficulty Selection
def Difficulty_Selection():
    print("Choose your difficulty:")
    print("1. Easy")
    print("2. Normal")
    print("3. Hard")
    choice = input("Enter the number corresponding to your choice: ")
    
    if choice == "1":
        return "Easy"
    elif choice == "2":
        return "Normal"
    elif choice == "3":
        return "Hard"
    else:
        print("Invalid choice. Please try again.")
        return Difficulty_Selection()

def Stats():
    # Retrieve data from the character object
    health = character.health
    damage = character.damage_output
    rooms_completed = character.rooms_completed
    enemies_killed = character.enemies_killed
    
    # Print character stats
    print("\n")
    print("You have", health, "health" + "\n")
    time.sleep(1)
    print("You deal", damage, "damage" + "\n")
    time.sleep(1)
    print("You have completed", rooms_completed, "room(s)" + "\n")
    time.sleep(1)
    print("You have killed", enemies_killed, "enemy(ies)" + "\n")
    time.sleep(1)

# Fight
def Fight():
    Hit = random.randint(1,10)
    if Hit > 6:
        # Retrieve enemy health from generate_enemies or retrieve_enemies function
        enemy_health = 0
        enemies = generate_enemies() or retrieve_enemies()
        if enemies:
            for enemy in enemies:
                enemy_health += enemy_obj.enemy_health
        enemy_health -= character.damage_output
        print("You have dealt", character.damage_output, "damage to the enemy" + "\n")
        print("The enemy has", enemy_health, "health remaining" + "\n")
        time.sleep(1)
    else:
        print("You have missed")
    
    Take_Damage()

    # Retrieve enemy health
    enemy_health = enemy_objects.enemy_health
    print("Enemy health:", enemy_health)

# Run Away
def Run_Away():
    global Escaped
    global Battle
    Escaped = random.randint(1,10)
    if Escaped > 7:
        print("You have escaped")
        Battle = False
    else:
        print("You have failed to escape")
        Take_Damage()
        Battle = True

# Encounter
def Encounter():
    global Choice
    global Battle
    global Enemies
    global Area_Count
    global Original_Enemies
    global Diff_Choose
    Diff_Choose = Difficulty_Selection()
    Enemies = 0
    print("You have entered a new room" + "\n")
    time.sleep(1)

    if Diff_Choose == "Easy":
        Enemy_Damage = 1
        Enemy_Health = 3
    elif Diff_Choose == "Normal":
        Enemy_Damage = 2
        Enemy_Health = 5
    elif Diff_Choose == "Hard":
        Enemy_Damage = 3
        Enemy_Health = 7
    
    Enemy_Count = 0
    Battle = True

    if character.health > 0:
        Room()
        print("You prepare for the fight ahead" + "\n")
        time.sleep(1)
        while Battle == True:
            if Enemies > 0:
                print("There are",Enemies,"Enemy(ies) in this room" + "\n")
                time.sleep(1)
                if Enemy_Health > 0 and character.health > 0:
                    Choice = input("""You are stood in front of the enemy. What do you want to do?

FIGHT, RUN AWAY OR USE BAG

""").upper()
                    Original_Enemy_Health = Enemy_Health
                    if Choice == "FIGHT":
                        Enemy_Health = Original_Enemy_Health
                        Fight()
                        if Enemy_Health < 1:
                            Enemies -= 1
                            Enemy_Health = Original_Enemy_Health
                        if Original_Enemies > Enemies:
                            print("You have killed an enemy" + "\n")
                            time.sleep(1)
                            print(Enemies,"Enemy(ies) still remain")
                            Original_Enemies = Enemies
                            Enemy_Count += 1
                        else:
                            time.sleep(1)
                    elif Choice == "RUN AWAY":
                        Run_Away()
                    elif Choice == "USE BAG":
                        Bag()
                elif character.health == 0:
                        print("You have died")
                        print("You have killed",Enemy_Count,"enemy(ies)")
                        Battle = False
                        Buff_Reset()
                        Choice = input("Do you want to try again?. Yes/No: ").upper()

                        while Choice != "YES" and Choice != "NO":
                            print("Please try that again")
                            Choice = input("Do you want to try again?. Yes/No: ").upper()

                        if Choice == "YES":
                            Encounter()
                        else:
                            print("See you next time!")
                            sys.exit()

            elif Enemies < 1:
                print("You have killed all the enemies")
                Battle = False
                Action()
                Room_Count()
    elif character.health == 0:
        print("You have died")
        print("You have killed",Enemy_Count,"enemy(ies)")
        Buff_Reset()
        Choice = input("Do you want to try again?. Yes/No: ").upper()
        if Choice == "YES":
            Encounter()
        elif Choice == "NO":
            print("See you next time!")
            sys.exit()
        else:
            print("Please try that again")
            Choice = input("Do you want to try again?. Yes/No: ").upper()

def generate_room_data():
    room_data = [
        ("Room 1", "This is the first room."),
        ("Room 2", "This is the second room."),
        ("Room 3", "This is the third room."),
        # Add more room data as needed
    ]
    
    # Generate random values for room names and descriptions
    for i in range(len(room_data)):
        room_name = f"Room {i+1}"
        room_description = f"This is the {room_name.lower()}."
        room_data[i] = (room_name, room_description)
        
    # Shuffle the room data randomly
    random.shuffle(room_data)
    
    # Insert room data into the 'rooms' table
    conn = sqlite3.connect('rooms.db')
    cursor = conn.cursor()
    
    cursor.executemany("INSERT INTO rooms (name, description) VALUES (?, ?)", room_data)
    
    conn.commit()
    conn.close()

# Room
def Room():
    global Next_Area

    Next_Area = True

    conn = sqlite3.connect('rooms.db')
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS rooms")
    cursor.execute('''CREATE TABLE rooms
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    description TEXT)''')

    # Check if 'rooms' table is empty
    cursor.execute("SELECT COUNT(*) FROM rooms")
    count = cursor.fetchone()[0]

    if count == 0:
        # Generate room data if 'rooms' table is empty
        generate_room_data()

    # Retrieve the rooms from the database
    cursor.execute('SELECT * FROM rooms')
    rooms = cursor.fetchall()

    conn.close()

    while Next_Area:
        randomChoice = random.randint(0, len(rooms) - 1)
        randomChosenRoom = rooms[randomChoice]
        RoomName = randomChosenRoom[1]
        RoomDescription = randomChosenRoom[2]
        print("Welcome to the", RoomName, "Room.")
        print("Room Description:", RoomDescription)
        Next_Area = False

def Room_Count():
    global Area_Count
    Area_Count += 1
    print("You have reached the end of the room")
    print("You have completed",Area_Count,"room(s)")
    time.sleep(1)

# Action
def Action():
    Choose = input("Enter your action (FORWARD, TURN AROUND, LEAVE, USE BAG): ").upper()
    while Choose != "FORWARD" and Choose != "TURN AROUND" and Choose != "LEAVE" and Choose != "USE BAG":
        print("Please Re-Confirm: ")
        Choose = input("Enter your action (FORWARD, TURN AROUND, LEAVE, USE BAG): ").upper()

    if Choose == "FORWARD":
        Encounter()
    elif Choose == "TURN AROUND":
        Encounter()
    elif Choose == "LEAVE":
        print("Oh. Well you're no fun :(")
        sys.exit()
    elif Choose == "USE BAG":
        Bag()
        Action()

# Take Damage
def Take_Damage():
    Hit = random.randint(1,10)
    if Enemies > 0:
        print(Enemies,"Enemy(ies) still remain" + "\n")
        if Hit > 3:
            if Diff_Choose == "Easy":
                enemy_id = 1  # Replace "1" with the actual value of enemy_id
                Hit = random.randint(1,10)
                if Hit > 3:
                    cursor.execute("SELECT damage_output FROM enemies WHERE id = ?", (enemy_id,))
                    enemy_damage = cursor.fetchone()[0]
                    character.health -= enemy_damage
                else:
                    print("The enemy has missed")
                    time.sleep(1)
                    Bonus()
            elif Diff_Choose == "Normal":
                Hit = random.randint(1,10)
                if Hit > 7:
                    cursor.execute("SELECT damage_output FROM enemies WHERE id = ?", (enemy_id,))
                    enemy_damage = cursor.fetchone()[0]
                    character.health -= enemy_damage
                else:
                    print("The enemy has missed")
                    time.sleep(1)
                    Bonus()
            elif Diff_Choose == "Hard":
                Hit = random.randint(1,10)
                if Hit > 8:
                    cursor.execute("SELECT damage_output FROM enemies WHERE id = ?", (enemy_id,))
                    enemy_damage = cursor.fetchone()[0]
                    character.health -= enemy_damage
                else:
                    print("The enemy has missed")
                    time.sleep(1)
                    Bonus()
            print("The enemy has dealt", enemy_damage, "damage to you" + "\n")
            print("You have", character.health, "health remaining" + "\n")
        else:
            print("The enemy has missed")
            time.sleep(1)
            Bonus()


# Connect to the database (creates a new database if it doesn't exist)
conn = sqlite3.connect('enemies.db')
cursor = conn.cursor()

# Create the enemies table if it doesn't exist
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

def create_character():
    global character
    # Prompt the player to enter their character details
    print("Welcome to the game!")
    print("Please create your character!")
    time.sleep(1)
    name = input("Enter your character's name: ")
    age = int(input("Enter your character's age: "))

    # Prompt the player to choose a sex
    print("Choose a sex:")
    sex_options = ["Male", "Female"]
    for i, sex_option in enumerate(sex_options):
        print(f"{i+1}. {sex_option}")
    sex_choice = int(input("Enter the number corresponding to your sex choice: "))
    if sex_choice < 1 or sex_choice > len(sex_options):
        print("Invalid input. Please choose a valid option.")
        return create_character()
    sex = sex_options[sex_choice - 1]

    # Prompt the player to choose a class
    print("Choose a class:")
    class_options = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard", "Artificer", "Blood Hunter"]
    for i, class_option in enumerate(class_options):
        print(f"{i+1}. {class_option}")
    class_choice = int(input("Enter the number corresponding to your class choice: "))
    if class_choice < 1 or class_choice > len(class_options):
        print("Invalid input. Please choose a valid option.")
        return create_character()
    class_type = class_options[class_choice - 1]

    level = 1
    experience = 0
    health = 100
    damage_output = 10

    # Create the character object
    character = Character(name, age, sex, class_type, level, experience, health, damage_output)

    print("\n", "Your character has been created!")
    Stats()
    Action()

    return character

create_character()