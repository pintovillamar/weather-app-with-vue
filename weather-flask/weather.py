from flask import Flask,render_template,request,abort,jsonify
# import json to load json data to python dictionary
import json

from flask_cors import cross_origin

# urllib.request to make a request to api
import urllib.request
from flask_cors import CORS


app = Flask(__name__)
def tocelcius(temp):
    return str(round(float(temp) - 273.16))

def tofarenheit(temp):
    return str(round((float(temp) - 273.16) * 9/5 + 32))

@app.route("/far/<city>", methods=['POST', 'GET'])
@cross_origin()
def far(city):
    api_key = '48a90ac42caa09f90dcaeee4096b9e53'
    if request.method == 'POST':
        city = request.form['city']
    else:
        #for default name arequipa
        city = 'arequipa'

    # source contain json data from api
    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid='+api_key).read()
    except:
        return abort(404)
    
    # converting json data to dictionary
    list_of_data = json.loads(source)

    # data for variable list_of_data
    data = {
        "temp_far": tofarenheit(list_of_data['main']['temp']) + '°F'
    }
    return jsonify(data)

@app.route("/test_temp", methods=['POST', 'GET'])
@cross_origin()
def test_temp():
    api_key = '48a90ac42caa09f90dcaeee4096b9e53'
    if request.method == 'POST':
        city = request.form['city']
    else:
        #for default name arequipa
        city = 'arequipa'

    # source contain json data from api
    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid='+api_key).read()
    except:
        return abort(404)
    
    # converting json data to dictionary
    list_of_data = json.loads(source)

    # data for variable list_of_data
    data = {
        "temp_cel": tocelcius(list_of_data['main']['temp']) + '°C'
    }
    return jsonify(data)

@app.route("/test_city2/<city>", methods=['POST', 'GET'])
@cross_origin()
def test_city2(city):
    api_key = '48a90ac42caa09f90dcaeee4096b9e53'
    # source contain json data from api
    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid='+api_key).read()
    except:
        return abort(404)
    
    # converting json data to dictionary
    list_of_data = json.loads(source)

    # data for variable list_of_data
    data = {
        "temp_cel": tocelcius(list_of_data['main']['temp']) + '°C',
        # "temp_cel": str(-11) + '°C'
    }
    return jsonify(data)

@app.route("/test_coord/<lat>/<long>", methods=['POST', 'GET'])
@cross_origin()
def test_coord(lat, long):
    api_key = '48a90ac42caa09f90dcaeee4096b9e53'
    # source contain json data from api
    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + long + '&appid='+api_key).read()
    except:
        return abort(404)
    
    # converting json data to dictionary
    list_of_data = json.loads(source)

    # data for variable list_of_data
    data = {
        "temp_cel": tocelcius(list_of_data['main']['temp']) + '°C',
        "city_name": str(list_of_data['name'])
    }
    return jsonify(data)

@app.route("/get_city_name/<lat>/<long>", methods=['POST', 'GET'])
@cross_origin()
def get_city_name(lat, long):
    api_key = '48a90ac42caa09f90dcaeee4096b9e53'
    # source contain json data from api
    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + long + '&appid='+api_key).read()
    except:
        return abort(404)
    
    # converting json data to dictionary
    list_of_data = json.loads(source)

    # data for variable list_of_data
    data = {
        # "temp_cel": tocelcius(list_of_data['main']['temp']) + '°C',
        "city_name": str(list_of_data['name'])
    }
    print(data)
    return jsonify(data)


@app.route('/',methods=['POST','GET'])
def weather():
    api_key = '48a90ac42caa09f90dcaeee4096b9e53'
    if request.method == 'POST':
        city = request.form['city']
    else:
        #for default name mathura
        city = 'mathura'

    # source contain json data from api
    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid='+api_key).read()
    except:
        return abort(404)
    # converting json data to dictionary

    list_of_data = json.loads(source)

    # data for variable list_of_data
    data = {
        "country_code": str(list_of_data['sys']['country']),
        "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
        "temp": str(list_of_data['main']['temp']) + 'k',
        "temp_cel": tocelcius(list_of_data['main']['temp']) + 'C',
        "pressure": str(list_of_data['main']['pressure']),
        "humidity": str(list_of_data['main']['humidity']),
        "cityname":str(city),
    }
    return render_template('index.html',data=data)



if __name__ == '__main__':
    app.run(port=5001,debug=True)
