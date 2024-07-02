from flask import Flask, jsonify, request
from db_utils import get_all_pets, add_pet, update_adoption_status

app = Flask(__name__)

#endpoint to retrieve our list of pets
@app.route('/pets', methods=['GET'])
def get_pets():
    res = get_all_pets()
    return jsonify(res)

#endpoint to post a new pet
@app.route('/pets', methods=['POST'])
def add_pet_endpoint():
    new_pet = request.get_json()
    pet_id = add_pet(
        name=new_pet['name'],
        species=new_pet['species'],
        age=new_pet['age']
    )
    return jsonify({"message": "Pet added successfully", "id": pet_id})

#endpoint to change the adoption status
@app.route('/pets/<int:pet_id>/adopt', methods=['PUT'])
def update_adoption_status_endpoint(pet_id):
    adoption_status = request.get_json().get('adopted')
    update_adoption_status(pet_id, adoption_status)
    return jsonify({"message": "Hooray, this pet found their new home!"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
