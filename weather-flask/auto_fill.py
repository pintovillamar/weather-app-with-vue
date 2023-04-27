from flask import request, abort

import json
import datetime

from db.database import db, ma

from db.city import City
from db.daily import Daily

import urllib.request 

peru_cities = [
    'Amazonas',
    'Ancash',
    'Apurimac',
    'Arequipa',
    'Ayacucho',
    'Cajamarca',
    'Cusco',
    'Huancavelica',
    'Huanuco',
    'Ica',
    'Junin',
    'Lambayeque',
    'Lima',
    'Loreto',
    'Moquegua',
    'Piura',
    'Puno',
    'Tacna',
    'Tumbes',
    'Ucayali'
]

# Get API values
api_key = '48a90ac42caa09f90dcaeee4096b9e53'

def get_values_and_print(city):
    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid='+api_key).read()
    except:
        return abort(404)
    
    list_of_data = json.loads(source)

    data = {
        "city_name:": str(City.query.filter_by(city_name=city).first().city_name),
        "city_id": str(City.query.filter_by(city_name=city).first().city_id),
        "city_latitude": str(round(float(list_of_data['coord']['lat']),4)),
        "city_longitude": str(round(float(list_of_data['coord']['lon']),4)),
        "daily_date": str(datetime.datetime.now().strftime("%Y-%m-%d")),
        "daily_temp_c": str(round(float(list_of_data['main']['temp']) - 273.16,2)),
        "daily_temp_f": str(round(float(list_of_data['main']['temp']) - 273.16,2) * 9/5 + 32),
        "time_of_issue": str(datetime.datetime.now().strftime("%H:%M:%S")),
        "daily_humidity": str(list_of_data['main']['humidity']),
        "daily_pressure": str(list_of_data['main']['pressure']),
    }

    print(data)

# Insert data to DB using endpoint
def insert_data(city):
    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid='+api_key).read()
    except:
        return abort(404)
    
    list_of_data = json.loads(source)

    data = {
        "daily_date": str(datetime.datetime.now().strftime("%Y-%m-%d")),
        "daily_temp_c": str(round(float(list_of_data['main']['temp']) - 273.16,2)),
        "daily_temp_f": str(round(float(list_of_data['main']['temp']) - 273.16,2) * 9/5 + 32),
        "daily_humidity": str(list_of_data['main']['humidity']),
        "daily_pressure": str(list_of_data['main']['pressure']),
        "daily_created_at": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "daily_updated_at": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "city_id": str(City.query.filter_by(city_name=city).first().city_id) 
    }

    new_daily = Daily(**data)
    db.session.add(new_daily)
    db.session.commit()

def  json_cities():
    
    cities_with_name = [{'city_name': city} for city in peru_cities]
    latitudes = [City.query.filter_by(city_name=city).first().city_latitude for city in peru_cities]
    longitudes = [City.query.filter_by(city_name=city).first().city_longitude for city in peru_cities]

    for i in range(len(cities_with_name)):
        cities_with_name[i]['city_latitude'] = latitudes[i]
        cities_with_name[i]['city_longitude'] = longitudes[i]

    json_str = json.dumps(cities_with_name)

    print(json_str)



# json_cities()

for each_city in City.query.all():
    insert_data(each_city.city_name)