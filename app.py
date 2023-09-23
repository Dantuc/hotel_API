from flask import Flask
from flask_restful import Api
from resources.hotel import Hotels, Hotel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


    
api.add_resource(Hotels, "/hoteis")
api.add_resource(Hotel, "/hoteis/<string:hotel_id>")

if __name__ == "__main__":
    from sql_alchemy import database
    database.init_app(app)

    with app.app_context():
        database.create_all()
    
    app.run(debug=True)