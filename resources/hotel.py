from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required

path_params = reqparse.RequestParser()
path_params.add_argument("city",type=str, default=None, location="args")
path_params.add_argument("stars_min",type=float, default=0, location="args")
path_params.add_argument("daily_min",type=float, default=0, location="args")
path_params.add_argument("daily_max",type=float, default=99999999999, location="args")
path_params.add_argument("offset",type=float, default=1, location="args")
path_params.add_argument("limit",type=float, default=100, location="args")

class Hotels(Resource):
    def get(self):
        
        data = path_params.parse_args()
            
        hotels = HotelModel.query.filter(
                                        HotelModel.stars > data["stars_min"],
                                        HotelModel.daily > data['daily_min'],
                                        HotelModel.daily < data['daily_max']
                                        ).paginate(page=data["offset"], per_page=data["limit"])
        if data['city']:
            hotels = HotelModel.query.filter(
                                        HotelModel.city == data["city"],
                                        HotelModel.stars > data["stars_min"],
                                        HotelModel.daily > data['daily_min'],
                                        HotelModel.daily < data['daily_max']
                                        ).paginate(page=data["offset"], per_page=data["limit"])
        
        return {"hoteis": [hotel.json() for hotel in hotels]}
    

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