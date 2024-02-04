#!/usr/bin/python3
"""Place Blueprint"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from flasgger.utils import swag_from


@app_views.route('/places', methods=['GET'], strict_slashes=False)
@swag_from('documentation/place/get.yml', methods=['GET'])
def get_all():
    """ get all by id"""
    all_list = [obj.to_dict() for obj in storage.all(Place).values()]
    return jsonify(all_list)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/place/get.yml', methods=['GET'])
def get_method_place(place_id):
    """ get places by id"""
    place = storage.get_place(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/place/delete.yml', methods=['DELETE'],
           strict_slashes=False)
def del_method(place_id):
    """ delete place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/place/create.yml', methods=['POST'])
def create_ob():
    """create a new place instance"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    res = request.get_json()
    obj = Place(**res)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<string:place_id>',
                 methods=['PUT'], strict_slashes=False)
@swag_from('documentation/place/put.yml', methods=['PUT'])
def put(place_id):
    """Update an existing place"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
