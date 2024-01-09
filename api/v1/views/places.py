#!/usr/bin/python3
""" API REST for states """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
import models


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def list_places(city_id=None):
    """ Return places by city """
    my_city = storage.get('City', city_id)
    if my_city is not None:
        place_list = []
        for value in storage.all('Place').values():
            if value.city_id == city_id:
                place_list.append(value.to_dict())
        return jsonify(place_list)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'])
def search_place(place_id=None):
    """ Return  a place by id """
    my_place = storage.get('Place', place_id)
    if my_place is not None:
        return jsonify(my_place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ Delete an object """
    my_object = storage.get('Place', place_id)
    if my_object is not None:
        storage.delete(my_object)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


def update_object(obj, **data):
    not_keys = ["id", "created_at", "updated_at", "city_id", "user_id"]
    for key, value in data.items():
        if key not in not_keys:
            if isinstance(value, str):
                value = value.replace("_", " ")
            setattr(obj, key, value)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """ Create an object """
    if storage.get('City', city_id) is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json(force=True)
    if 'name' not in request.json:
        return jsonify({"Error": "Missing name"}), 400
    if 'user_id' not in request.json:
        return jsonify({"Error": "Missing user_id"}), 400
    if storage.get('User', data['user_id']) is None:
        abort(404)
    new_object = Place()
    update_object(new_object, **data)
    setattr(new_object, 'city_id', city_id)
    setattr(new_object, 'user_id', data['user_id'])
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """ Update an object """
    my_object = storage.get('Place', place_id)
    if my_object is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json(force=True)
    update_object(my_object, **data)
    my_object.save()
    return jsonify(my_object.to_dict()), 200
