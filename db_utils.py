import mysql.connector
from config import USER, PASSWORD, HOST

##connect to our sql database
def _connect_to_db(db_name):
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin='mysql_native_password',
        database=db_name
    )

##function to find and return all the avilable pets in the shelter
def get_all_pets():
    db_name = 'petadoption'
    db_connection = _connect_to_db(db_name)
    cur = db_connection.cursor(dictionary=True)
    print("Connected to DB")

    query = "SELECT * FROM pets WHERE adopted = FALSE"
    cur.execute(query)
    result = cur.fetchall()
    db_connection.close()
    print("DB connection is closed")
    return result

##function to insert a new pet as last in our list of pets
def add_pet(name, species, age):
    db_name = 'petadoption'
    db_connection = _connect_to_db(db_name)
    cur = db_connection.cursor()
    print("Connected to DB")

    query = "INSERT INTO pets (name, species, age) VALUES (%s, %s, %s)"
    cur.execute(query, (name, species, age))
    db_connection.commit()

    #gets the ID
    pet_id = cur.lastrowid
    db_connection.close()
    print("DB connection is closed")
    return pet_id

##function to update pets to adopted
def update_adoption_status(pet_id, adopted):
    db_name = 'petadoption'
    db_connection = _connect_to_db(db_name)
    cur = db_connection.cursor()
    print("Connected to DB")

    query = "UPDATE pets SET adopted = %s WHERE id = %s"
    cur.execute(query, (adopted, pet_id))
    db_connection.commit()
    db_connection.close()
    print("DB connection is closed")
