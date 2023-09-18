from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hotels = [
    {
    'hotel_id': 'alp01',
    'name': 'Alpha Hotel',
    'stars': 4.3,
    'daily': 400.30,
    'city': 'Belo Horizonte'
    },
    {
    'hotel_id': 'bet01',
    'name': 'Beta Hotel',
    'stars': 4.7,
    'daily': 478.30,
    'city': "Rio de Janeiro"
    },
    {
    'hotel_id': 'gam01',
    'name': 'Gama Hotel',
    'stars': 4.9,
    'daily': 632.32,
    'city': "Belo Horizonte"
    },
]

class Hotels(Resource):
    def get(self):
        return {'hotels': hotels}
    

class Hotel(Resource):
    arguments = reqparse.RequestParser()
    arguments.add_argument("name")
    arguments.add_argument("stars")
    arguments.add_argument("daily")
    arguments.add_argument("city")


    def find_hotel(hotel_id):
        for hotel in hotels:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)

        if hotel:
            return hotel
        return {'message': 'Hotel not found.'}, 404

    def post(self, hotel_id):

        data = Hotel.arguments.parse_args()

        hotel_obj = HotelModel(hotel_id, **data)
        new_hotel = hotel_obj.json()
        hotels.append(new_hotel)
        return new_hotel, 201

    def put(self, hotel_id):

        data = Hotel.arguments.parse_args()        

        hotel_obj = HotelModel(hotel_id, **data)
        new_hotel = hotel_obj.json()
        hotel = Hotel.find_hotel(hotel_id)

        if hotel:
            hotel.update(new_hotel)
            return new_hotel, 200
        return {'message': 'Hotel not found.'}, 404    

    def delete(self, hotel_id):
        for i, hotel in enumerate(hotels):
            if hotel['hotel_id'] == hotel_id:
                hotels.pop(i)
            return [], 204
        return {'message': 'Hotel not found.'}, 404