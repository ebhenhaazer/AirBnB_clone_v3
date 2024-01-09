#!/usr/bin/python3
""" API REST for Amenities """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
import models


@app_views.route('/users/', methods=['GET'])
@app_views.route('/users/<user_id>', methods=['GET'])
def list_users(user_id=None):
    """ Return only an amenity or a list of amenities """
    user_list = []
    try:
        if user_id is None:
            for value in storage.all('User').values():
                user_list.append(value.to_dict())
        else:
            user_list = storage.get('User', user_id).to_dict()
        return jsonify(user_list)
    except Exception:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Delete an object """
    my_object = storage.get('User', user_id)
    if my_object is not None:
        storage.delete(my_object)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


def update_object(obj, **data):
    not_keys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in not_keys:
            if isinstance(value, str):
                value = value.replace("_", " ")
            setattr(obj, key, value)


@app_views.route('/users/', methods=['POST'])
def create_user():
    """ Create an object """
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json(force=True)
    if 'email' not in request.json:
        return jsonify({"Error": "Missing email"}), 400
    if 'password' not in request.json:
        return jsonify({"Error": "Missing password"}), 400
    new_object = User()
    update_object(new_object, **data)
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_user(user_id):
    """ Update an object """
    my_object = storage.get('User', user_id)
    if my_object is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json(force=True)
    update_object(my_object, **data)
    my_object.save()
    return jsonify(my_object.to_dict()), 200
