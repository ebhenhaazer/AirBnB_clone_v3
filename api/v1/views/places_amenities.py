#!/usr/bin/python3
""" API REST for states """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
import models


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
@app_views.route('/places/<place_id>/amenities/', methods=['GET'])
def list_place_amenities(place_id=None):
    """ Return amenities by place """
    my_place = storage.get('Place', place_id)
    if my_place is not None:
        amenity_list = []
        for value in my_place.amenities:
            amenity_list.append(value.to_dict())
        return jsonify(amenity_list)
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_place_amenity(amenity_id, place_id):
    """ Delete an object """
    my_amenity = storage.get('Amenity', amenity_id)
    my_place = storage.get('Place', place_id)
    if my_amenity is None or my_place is None:
        abort(404)
    amenity_linked = False
    for amenity in my_place.amenities:
        if my_amenity.id == amenity.id:
            amenity_linked = True
    if amenity_linked is False:
        abort(404)
    place.amenities.remove(my_amenity)
    place.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_place_amenity(amenity_id, place_id):
    """ Link an amenity to a place """
    my_amenity = storage.get('Amenity', amenity_id)
    my_place = storage.get('Place', place_id)
    if my_amenity is None or my_place is None:
        abort(404)
    if my_amenity in my_place.amenities:
        return jsonify(my_amenity.to_dict()), 200
    my_place.amenities.append(my_amenity)
    return jsonify(my_amenity.to_dict()), 201
