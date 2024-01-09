#!/usr/bin/python3
""" API REST for states """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
import models


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
@app_views.route('/places/<place_id>/reviews/', methods=['GET'])
def list_reviews(place_id=None):
    """ Return places by city """
    my_place = storage.get('Place', place_id)
    if my_place is not None:
        review_list = []
        for value in storage.all('Review').values():
            if value.place_id == place_id:
                review_list.append(value.to_dict())
        return jsonify(review_list)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    '''Retrieves a review for a place'''
    try:
        review = storage.get('Review', review_id).to_dict()
        return jsonify(review)
    except Exception:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ Delete an object """
    my_object = storage.get('Review', review_id)
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


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """ Create an object """
    if storage.get('Place', place_id) is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json(force=True)
    if 'text' not in request.json:
        return jsonify({"Error": "Missing text"}), 400
    if 'user_id' not in request.json:
        return jsonify({"Error": "Missing user_id"}), 400
    if storage.get('User', data['user_id']) is None:
        abort(404)
    new_object = Review()
    update_object(new_object, **data)
    setattr(new_object, 'user_id', data['user_id'])
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id):
    """ Update an object """
    my_object = storage.get('Review', review_id)
    if my_object is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json(force=True)
    update_object(my_object, **data)
    my_object.save()
    return jsonify(my_object.to_dict()), 200
