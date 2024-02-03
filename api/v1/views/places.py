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
