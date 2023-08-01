#!/usr/bin/python3
"""
Flask view for Places module
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger.utils import swag_from
from models import storage, CNC
from os import environ
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


places_blueprint = Blueprint('places', __name__)


@places_blueprint.route('/api/v1/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    city = City.query.get(city_id)
    if not city:
        return jsonify({'error': 'City not found'}), 404

    places = city.places
    return jsonify([place.to_dict() for place in places]), 200


@places_blueprint.route('/api/v1/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = Place.query.get(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    return jsonify(place.to_dict()), 200


@places_blueprint.route('/api/v1/places', methods=['POST'])
def create_place():
    city_id = request.json['city_id']
    user_id = request.json['user_id']
    name = request.json['name']

    city = City.query.get(city_id)
    if not city:
        return jsonify({'error': 'City not found'}), 404

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    place = Place(name=name, city=city, user=user)
    place.save()

    return jsonify(place.to_dict()), 201


@places_blueprint.route('/api/v1/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    place = Place.query.get(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    data = request.json
    for key, value in data.items():
        if key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            continue

        setattr(place, key, value)

    place.save()

    return jsonify(place.to_dict()), 200


@places_blueprint.route('/api/v1/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = Place.query.get(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    place.delete()

    return jsonify({'message': 'Place deleted'}), 200
