#!/usr/bin/python3
""" API REST for Amenities """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
import models


@app_views.route('/amenities/', methods=['GET'])
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def list_amenities(amenity_id=None):
    """ Return only an amenity or a list of amenities """
    amenity_list = []
    try:
        if amenity_id is None:
            for value in storage.all('Amenity').values():
                amenity_list.append(value.to_dict())
        else:
            amenity_list = storage.get('Amenity', amenity_id).to_dict()
        return jsonify(amenity_list)
    except Exception:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Delete an object """
    my_object = storage.get('Amenity', amenity_id)
    if my_object is not None:
        storage.delete(my_object)
        storage.save()
        return jsonify({})
    else:
        abort(404)


def update_object(obj, **data):
    not_keys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in not_keys:
            if isinstance(value, str):
                value = value.replace("_", " ")
            setattr(obj, key, value)


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """ Create an object """
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json(force=True)
    if 'name' not in request.json:
        return jsonify({"Error": "Missing name"}), 400
    new_object = Amenity()
    update_object(new_object, **data)
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenity(amenity_id):
    """ Update an object """
    my_object = storage.get('Amenity', amenity_id)
    if my_object is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json(force=True)
    update_object(my_object, **data)
    my_object.save()
    return jsonify(my_object.to_dict()), 200
