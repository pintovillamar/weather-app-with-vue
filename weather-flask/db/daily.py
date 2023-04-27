from flask import jsonify
from flask import Blueprint
from flask import request
from flask_cors import cross_origin
import datetime

from werkzeug.utils import secure_filename

from db.database import db, ma

class Daily(db.Model):
    daily_id = db.Column(db.Integer, primary_key=True)
    daily_date = db.Column(db.Date, nullable=False)
    daily_temp_c = db.Column(db.Float, nullable=False) 
    daily_temp_f = db.Column(db.Float, nullable=False)
    daily_humidity = db.Column(db.Float, nullable=False)
    daily_feels_like = db.Column(db.Float, nullable=False)
    daily_pressure = db.Column(db.Float, nullable=False)
    daily_created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    daily_updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'), nullable=False)

    def __init__(self, daily_date, daily_temp_c, daily_temp_f, daily_humidity, daily_pressure, daily_created_at, daily_updated_at, city_id):
        self.daily_date = daily_date
        self.daily_temp_c = daily_temp_c
        self.daily_temp_f = daily_temp_f
        self.daily_humidity = daily_humidity
        self.daily_pressure = daily_pressure
        self.daily_created_at = daily_created_at
        self.daily_updated_at = daily_updated_at
        self.city_id = city_id

    def __repr__(self):
        return f"Daily('{self.daily_date}', '{self.daily_temp_c}', '{self.daily_temp_f}', '{self.daily_humidity}', '{self.daily_pressure}', '{self.daily_created_at}', '{self.daily_updated_at}', '{self.city_id}')"
    
class DailySchema(ma.Schema):
    class Meta:
        fields = ('daily_id', 'daily_date', 'daily_temp_c', 'daily_temp_f', 'daily_humidity', 'daily_pressure', 'daily_created_at', 'daily_updated_at', 'city_id')

daily_schema = DailySchema()
dailies_schema = DailySchema(many=True)

db.create_all()

class DailyModel():
    def create_daily(self):
        new_daily = Daily(
            request.json['daily_date'],
            request.json['daily_temp_c'],
            request.json['daily_temp_f'],
            request.json['daily_humidity'],
            request.json['daily_pressure'],
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            request.json['city_id']
        )
        db.session.add(new_daily)
        db.session.commit()
        return daily_schema.jsonify(new_daily)

    def dailies(self):
        dailies = Daily.query.all()
        return dailies_schema.jsonify(dailies)
    
    def daily(self, daily_id):
        daily = Daily.query.get(daily_id)
        return daily_schema.jsonify(daily)
    
    def update_daily(self, daily_id):
        daily = Daily.query.get(daily_id)
        daily.daily_date = request.json['daily_date']
        daily.daily_temp_c = request.json['daily_temp_c']
        daily.daily_temp_f = request.json['daily_temp_f']
        daily.daily_humidity = request.json['daily_humidity']
        daily.daily_pressure = request.json['daily_pressure']
        daily.daily_updated_at = datetime.datetime.now()
        daily.city_id = request.json['city_id']
        db.session.commit()
        return daily_schema.jsonify(daily)
    
    def delete_daily(self, daily_id):
        daily = Daily.query.get(daily_id)
        db.session.delete(daily)
        db.session.commit()
        return daily_schema.jsonify(daily)
    
### Blueprint ###

model = DailyModel()

daily_blueprint = Blueprint('daily_blueprint', __name__)

@daily_blueprint.route('/create_daily', methods=['POST'])
@cross_origin()
def create_daily():
    return model.create_daily()

@daily_blueprint.route('/dailies', methods=['GET'])
@cross_origin()
def dailies():
    return model.dailies()

@daily_blueprint.route('/daily/<daily_id>', methods=['GET'])
@cross_origin()
def daily(daily_id):
    return model.daily(daily_id)

@daily_blueprint.route('/daily/<daily_id>', methods=['PUT'])
@cross_origin()
def update_daily(daily_id):
    return model.update_daily(daily_id)

@daily_blueprint.route('/daily/<daily_id>', methods=['DELETE'])
@cross_origin()
def delete_daily(daily_id):
    return model.delete_daily(daily_id)


