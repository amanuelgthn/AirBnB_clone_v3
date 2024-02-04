#!/usr/bin/python3
"""
Place blueprint
"""

from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from flasgger.utils import swag_from
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_all(city_id):
    """ return all the place objects withing a given city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places_all = [obj.to_json() for obj in storage.all("Place").values()
                  if obj.city_id == city_id]
    return jsonify(places_all)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_method_place(place_id):
    """ Returns a place by place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_method(place_id):
    """ delete place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_ob(city_id):
    """create a new place instance"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    value = request.get_json()
    if value is None:
        abort(400, "Not a JSON")
    if 'user_id' not in value.keys():
        abort(400, "Missing user_id")
    user = storage.get("User", value["user_id"])
    if user is None:
        abort(404)
    if 'name' not in value.keys():
        abort(400, "Missing name")
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    obj = Place(**value)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<string:place_id>',
                 methods=['PUT'], strict_slashes=False)
def put(place_id):
    """Update an existing place"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
