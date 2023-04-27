from flask import Blueprint
from flask import request
from flask import jsonify
from flask_cors import cross_origin
from werkzeug import exceptions
import requests
import json

from db.database import db, ma

from datetime import datetime

from db.city import City
from db.daily import Daily

class test(db.Model):
    test_id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(255), nullable=False)
    test_description = db.Column(db.String(255), nullable=False)
    test_created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    test_updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, test_name, test_description, test_created_at, test_updated_at):
        self.test_name = test_name
        self.test_description = test_description
        self.test_created_at = test_created_at
        self.test_updated_at = test_updated_at

    def __repr__(self):
        return f"test('{self.test_name}', '{self.test_description}', '{self.test_created_at}', '{self.test_updated_at}')"
    

class testSchema(ma.Schema):
    class Meta:
        fields = ('test_id', 'test_name', 'test_description', 'test_created_at', 'test_updated_at')

test_schema = testSchema()
tests_schema = testSchema(many=True)

class testModel:
    pass

### BLUEPRINTS ###

model = testModel()

test_blueprint = Blueprint('test', __name__)

@test_blueprint.route('/test/<name>', methods=['POST'])
@cross_origin()
def test(name):
    # city_id = id
    # name = City.query.get(city_id).city_name
    # longitude = City.query.get(city_id).city_longitude
    # latitude = City.query.get(city_id).city_latitude
    
    # return jsonify({'city name: ': name, 'city longitude: ': longitude , 'city latitude: ': latitude})

    # only with the name obtain the id of the city
    city_id = City.query.filter_by(city_name=name).first().city_id
    return jsonify({'city id: ': city_id})
