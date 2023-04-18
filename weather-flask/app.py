from flask_cors import CORS
from db.database import app

from db.city import city_blueprint
from db.test import test_blueprint

app.register_blueprint(city_blueprint)
app.register_blueprint(test_blueprint)

cors = CORS(app, supports_credentials=True)

if __name__ == '__main__':
    app.run(debug=True)