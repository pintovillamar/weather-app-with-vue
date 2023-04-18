from flask import jsonify
from flask import Blueprint
from flask import request
from flask_cors import cross_origin
import datetime

from werkzeug.utils import secure_filename

from db.database import db, ma

class City(db.Model):
    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(255), nullable=False)
    city_longitude = db.Column(db.Float, nullable=False)
    city_latitude = db.Column(db.Float, nullable=False)
    city_created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    city_updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, city_name, city_longitude, city_latitude, city_created_at, city_updated_at):
        self.city_name = city_name
        self.city_longitude = city_longitude
        self.city_latitude = city_latitude
        self.city_created_at = city_created_at
        self.city_updated_at = city_updated_at

    def __repr__(self):
        return f"City('{self.city_name}', '{self.city_longitude}', '{self.city_latitude}', '{self.city_created_at}', '{self.city_updated_at})"
    
class CitySchema(ma.Schema):
    class Meta:
        fields = ('city_id', 'city_name', 'city_longitude', 'city_latitude', 'city_created_at', 'city_updated_at')

city_schema = CitySchema()
cities_schema = CitySchema(many=True)

db.create_all()

class CityModel():
    def create_city(self):
        new_city = City(
            request.json['city_name'],
            request.json['city_longitude'],
            request.json['city_latitude'],
            datetime.datetime.now(),
            datetime.datetime.now()
        )
        db.session.add(new_city)
        db.session.commit()
        return city_schema.jsonify(new_city)
    
    def cities(self):
        cities = City.query.all()
        return cities_schema.jsonify(cities)
    
    def city(self, city_id):
        city = City.query.get(city_id)
        return city_schema.jsonify(city)
    
    def update_city(self, city_id):
        city = City.query.get(city_id)
        city.city_name = request.json['city_name']
        city.city_longitude = request.json['city_longitude']
        city.city_latitude = request.json['city_latitude']
        city.city_updated_at = datetime.datetime.now()
        db.session.commit()
        return city_schema.jsonify(city)
    
    def delete_city(self, city_id):
        city = City.query.get(city_id)
        db.session.delete(city)
        db.session.commit()
        return city_schema.jsonify(city)
    
### Blueprint ###

model = CityModel()

city_blueprint = Blueprint('/city_blueprint', __name__)

@city_blueprint.route('/create_city', methods=['POST'])
@cross_origin()
def create_city():
    return model.create_city()

@city_blueprint.route('/cities', methods=['GET'])
@cross_origin()
def cities():
    return model.cities()

@city_blueprint.route('/city/<city_id>', methods=['GET'])
@cross_origin()
def city(city_id):
    return model.city(city_id)

@city_blueprint.route('/update_city/<city_id>', methods=['PUT'])
@cross_origin()
def update_city(city_id):
    return model.update_city(city_id)

@city_blueprint.route('/delete_city/<city_id>', methods=['DELETE'])
@cross_origin()
def delete_city(city_id):
    return model.delete_city(city_id)
