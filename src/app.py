"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all():
    members = jackson_family.get_all_members()
    if status_code is 200:
        return jsonify(members), 200
    if 400 < status_code < 499:
        return jsonify({"msg":"No family members found"}), status_code
    if status_code > 500:
        return jsonify({"msg":"Server error"}), status_code

@app.route('/member/<int:member_id>', methods=['GET'])
def get_one(member_id):
    member=jackson_family.get_member(member_id)
    if status_code is 200:
        return jsonify(member), 200
    if 400 < status_code < 499:
        return jsonify({"msg":"No family member found"}), status_code
    if status_code > 500:
        return jsonify({"msg":"Server error"}), status_code

@app.route('/member', methods=['POST'])
def add_member():
    new_memberRequest = request.get_json()
    new_member=jackson_family.add_member(new_memberRequest)
    if status_code is 200:
        return jsonify(new_member), 200
    if 400 < status_code < 499:
        return jsonify({"msg":"No family member found"}), status_code
    if status_code > 500:
        return jsonify({"msg":"Server error"}), status_code

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    jackson_family.delete_member(member_id)
    return jsonify({"done":True}),200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
