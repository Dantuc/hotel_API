from flask_restful import Resource, reqparse

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
    def get(self, hotel_id):
        for hotel in hotels:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return {'message': 'Hotel not found.'}, 404

    def post(self, hotel_id):
        arguments = reqparse.RequestParser()
        arguments.add_argument("name")
        arguments.add_argument("stars")
        arguments.add_argument("daily")
        arguments.add_argument("city")

        data = arguments.parse_args()

        new_hotel = {
            'hotel_id': hotel_id,
            'name': data['name'],
            'stars': data['stars'],
            'daily': data['daily'],
            'city': data['city']
        }

        hotels.append(new_hotel)
        return new_hotel, 201



    def put(self, hotel_id):
        for hotel in hotels:
            if hotel['hotel_id'] == hotel_id:
                arguments = reqparse.RequestParser()
                arguments.add_argument("name")
                arguments.add_argument("stars")
                arguments.add_argument("daily")
                arguments.add_argument("city")

                data = arguments.parse_args()

                if data['name'] is not None: 
                    hotel['name'] = data['name']
                if data['stars'] is not None:     
                    hotel['stars'] = data['stars']
                if data['daily'] is not None: 
                    hotel['daily'] = data['daily']
                if data['city'] is not None: 
                    hotel['city'] = data['city']

                return hotel
        return {'message': 'Hotel not found.'}, 404    

    def delete(self, hotel_id):
        for i, hotel in enumerate(hotels):
            if hotel['hotel_id'] == hotel_id:
                hotels.pop(i)
            return [], 204
        return {'message': 'Hotel not found.'}, 404