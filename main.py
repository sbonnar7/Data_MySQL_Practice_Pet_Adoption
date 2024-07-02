import json
import requests

##function to call the GET endpoint defined in app file and returns all the pets in the DB
def get_pets():
    result = requests.get('http://localhost:5001/pets')
    return result.json()

##function to display the pets in a table
def display_pets(pets):
    print("{:<5} {:<15} {:<10} {:<5} {:<10}".format('ID', 'Name', 'Species', 'Age', 'Adopted'))
    print('-' * 50)

    for pet in pets:
        print("{:<5} {:<15} {:<10} {:<5} {:<10}".format(
            pet['id'], pet['name'], pet['species'], pet['age'], 'No' if not pet['adopted'] else 'Yes'
        ))

##function to add new pet to the DB using a POST endpoint
def add_new_pet(name, species, age):
    pet = {
        "name": name,
        "species": species,
        "age": age,
    }
    response = requests.post(
    'http://localhost:5001/pets',
        headers={'content-type': 'application/json'},
        data=json.dumps(pet)
    )
    response.raise_for_status()
    return response.json()

##function to change the adoption status of specified pet_id using a PUT endpoint
def update_adoption_status(pet_id, adopted):
    adoption_status = {
        "adopted": adopted
    }
    response = requests.put(
    f'http://localhost:5001/pets/{pet_id}/adopt',
        headers={'content-type': 'application/json'},
        data=json.dumps(adoption_status)
        )
    response.raise_for_status()
    return response.json()

##function runs through the questions and each function if they say Y
def run():
    print('############################')
    print('Welcome to the Pet Adoption System')
    print('############################')
    pets = get_pets()
    print('###### AVAILABLE PETS #######')
    display_pets(pets)

    add_pet = input('Would you like to add a new pet to the system (y/n)? ')
    if add_pet.lower() == 'y':
        name = input('Enter pet name: ')
        species = input('Enter pet species: ')
        age = int(input('Enter pet age: '))
        result = add_new_pet(name, species, age)
        print(result)

    adopt_pet = input('Would you like to update a pet\'s adoption status (y/n)? ')
    if adopt_pet == 'y':
        pet_id = int(input('Enter pet ID to update: '))
        adopted = input('Is the pet adopted (true/false)? ').lower() == 'true'
        result = update_adoption_status(pet_id, adopted)
        print(result)

    print()
    print('Thank you for using the Pet Adoption System!')

if __name__ == '__main__':
    run()
