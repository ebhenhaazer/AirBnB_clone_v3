#!/usr/bin/python3
""" API REST for states """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
import models


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def list_cities(state_id=None):
    """ Return cities by state """
    my_state = storage.get('State', state_id)
    if my_state is not None:
        city_list = []
        for value in storage.all('City').values():
            if value.state_id == state_id:
                city_list.append(value.to_dict())
        return jsonify(city_list)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'])
def search_city(city_id=None):
    """ Return cities by state """
    my_city = storage.get('City', city_id)
    if my_city is not None:
        return jsonify(my_city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ Delete an object """
    my_object = storage.get('City', city_id)
    if my_object is not None:
        storage.delete(my_object)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


def update_object(obj, **data):
    not_keys = ["id", "created_at", "updated_at", "state_id"]
    for key, value in data.items():
        if key not in not_keys:
            if isinstance(value, str):
                value = value.replace("_", " ")
            setattr(obj, key, value)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """ Create an object """
    if storage.get('State', state_id) is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json(force=True)
    if 'name' not in request.json:
        return jsonify({"Error": "Missing name"}), 400
    new_object = City()
    update_object(new_object, **data)
    setattr(new_object, 'state_id', state_id)
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city(city_id):
    """ Update an object """
    my_object = storage.get('City', city_id)
    if my_object is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json(force=True)
    update_object(my_object, **data)
    my_object.save()
    return jsonify(my_object.to_dict()), 200
