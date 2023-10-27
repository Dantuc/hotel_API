from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3
import os.path

def normalize_path_params(city=None, stars_min=0, daily_min=0, daily_max=100000, limit=50, offset=0, **data):

    if city:
        return {
            'city': city,
            'stars_min': stars_min,
            'daily_min': daily_min,
            'daily_max': daily_max,
            'limit': limit,
            'offset': offset
        }
    return {
            'stars_min': stars_min,
            'daily_min': daily_min,
            'daily_max': daily_max,
            'limit': limit,
            'offset': offset
        }

path_params = reqparse.RequestParser()
path_params.add_argument('city', type=str, location='json')
path_params.add_argument('stars_min', type=float, location='json')
path_params.add_argument('daily_min', type=float, location='json')
path_params.add_argument('daily_max', type=float, location='json')
path_params.add_argument('limit', type=int, location='json')
path_params.add_argument('offset', type=int, location='json')

class Hotels(Resource):
    def get(self):

        connection = sqlite3.connect('C:\Formacao_dev\hotel_API\hotel_API\instance\database.db')
        cursor = connection.cursor()


        data = path_params.parse_args()
        valid_data = {key:data[key] for key in data if data[key] is not None}
        params = normalize_path_params(**valid_data)
        
        if not params.get('city'):
            query = "SELECT * FROM hotels WHERE stars > ? and daily < ? and daily > ? LIMIT ? OFFSET ?"
            tuple_query = tuple([params[key] for key in params])
            result = cursor.execute(query, tuple_query)
        else: 
            query = "SELECT * FROM hotels WHERE city = ? and stars > ? and daily < ? and daily > ? LIMIT ? OFFSET ?"
            tuple_query = tuple([params[key] for key in params])
            result = cursor.execute(query, tuple_query)

        hotels = []
        for line in result:
            hotels.append({
                'hotel_id' : line[0],
                'name' : line[1],
                'stars' : line[2],
                'daily' : line[3],
                'city' : line[4]  
            })

        return {'hotels': hotels}
    

class Hotel(Resource):
    arguments = reqparse.RequestParser()
    arguments.add_argument("name", type=str, required=True, help= "The fild 'name' cannot be blank")
    arguments.add_argument("stars")
    arguments.add_argument("daily")
    arguments.add_argument("city")



    def get(self, hotel_id):
        
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            return hotel.json()
        
        return {"message" : f"Hotel {hotel_id} not found."}, 404

    @jwt_required()
    def post(self, hotel_id):

        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            return {"message" : f"Holtel ID {hotel_id} already exists."}, 400

        data = Hotel.arguments.parse_args()
        hotel_obj = HotelModel(hotel_id, **data)

        try:
            hotel_obj.save_hotel()
        except:
            return {'message': 'An internal error ocurred, please try again later'}, 500
        return hotel_obj.json()
        
    @jwt_required()
    def put(self, hotel_id):

        data = Hotel.arguments.parse_args()        
        hotel_finded = HotelModel.find_hotel(hotel_id)

        if hotel_finded:
            hotel_finded.update_hotel(**data)
            try:
                hotel_finded.save_hotel()
            except: 
                return {'message': 'An internal error ocurred, please try again later'}, 500
            return hotel_finded.json(), 200
        return {'message': 'Hotel not found.'}, 404    

    @jwt_required
    def delete(self, hotel_id):

        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            try:
                hotel.delete_hotel()
            except: return {'message': 'An internal error ocurred, please try again later'}, 500
            return {'message': f'Hotel {hotel_id} deleted.'}
        return {'message': 'Hotel not found.'}, 404