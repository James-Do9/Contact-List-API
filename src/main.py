"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Contact
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/contact/all', methods=['GET'])
def all_contacts():
#Method should return all of the contacts
    contacts = Contact.query.all()
    contacts = list(map(lambda x: x.serialize(), contacts))
    return jsonify(contacts), 200

@app.route('/contact', methods=['POST'])
def new_contact():
#Method should create a new contact
    body = request.get_json() #Grabs info
    info = Contact(full_name=body['full_name'], email=body['email'], address=body['address'] ,phone=body['phone']) #Assigns info
    db.session.add(info) #Adds info into the database
    db.session.commit() #Commits it
    updated_contact = Contact.query.all() #Returns the updated list
    updated_contact = list(map(lambda x: x.serialize(), updated_contact)) #Serializes it
    return jsonify(updated_contact), 200 

@app.route('/contact/<int:contact_id>', methods=['GET'])
def grab_contact(contact_id):
#Method should return a contact at the specific ID
    fetch_contact = Contact.query.filter_by(id=contact_id).all()
    fetch_contact = list(map(lambda x: x.serialize(), fetch_contact))
    return jsonify(fetch_contact), 200

@app.route('/contact/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
#Method should delete the contact
    to_be_deleted = Contact.query.get(contact_id)
    if to_be_deleted is None:
        raise APIException('Contact not found', status_code=404)
    db.session.delete(to_be_deleted)
    db.session.commit()
    updated_contact = Contact.query.all()
    updated_contact = list(map(lambda x: x.serialize(), updated_contact))
    return jsonify(updated_contact), 200

@app.route('/contact/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
#Method should update the contact
    body= request.get_json()
    fetch_contact = Contact.query.get(contact_id)
    if fetch_contact is None:
        raise APIException('Contact does not exist', status_code=404)
    if 'full_name' in body:
        fetch_contact.full_name = body['full_name']
        fetch_contact.email = body['email']
        fetch_contact.address = body['address']
        fetch_contact.phone = body['phone']
    db.session.commit()
    updated_contact = Contact.query.filter_by(id=contact_id)
    updated_contact = list(map(lambda x: x.serialize(), updated_contact))
    return jsonify(updated_contact), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
