#!/usr/bin/python3
""" API REST for states """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
import models


@app_views.route('/states/', methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'])
def list_states(state_id=None):
    """ Return only a state or a list of states """
    state_list = []
    try:
        if state_id is None:
            for value in storage.all('State').values():
                state_list.append(value.to_dict())
        else:
            state_list = storage.get('State', state_id).to_dict()
        return jsonify(state_list)
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Delete an object """
    my_object = storage.get('State', state_id)
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


@app_views.route('/states/', methods=['POST'])
def create_state():
    """ Create an object """
    data = request.get_json(force=True)
    if 'name' not in request.json:
        return jsonify({"Error": "Missing name"}), 400
    new_object = State()
    update_object(new_object, **data)
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    """ Update an object """
    my_object = storage.get('State', state_id)
    if my_object is None:
        abort(404)
    data = request.get_json(force=True)
    update_object(my_object, **data)
    my_object.save()
    return jsonify(my_object.to_dict()), 200
