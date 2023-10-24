from flask_restful import Resource, reqparse
from models.user import UserMoldel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from resources.security import create_password_hash, verify_password
from blacklist import BLACKLIST

arguments = reqparse.RequestParser()
arguments.add_argument('login', type=str, required=True, help= 'The fild "login" cannot be left blank.')
arguments.add_argument('password', type=str, required=True, help= 'The fild "password" cannot be left blank.')

class User(Resource):

    def get(self, user_id):
        
        user = UserMoldel.find_user(user_id)

        if user:
            return user.json()
        
        return {"message" : f"User {user_id} not found."}, 404
    
    @jwt_required()
    def delete(self, user_id):

        user = UserMoldel.find_user(user_id)

        if user:
            try:
                user.delete_user()
            except: return {'message': 'An internal error ocurred, please try again later'}, 500
            return {'message': f'User {user_id} deleted.'}
        return {'message': 'User not found.'}, 404
    
class UserRegister(Resource):

    def post(self):
        
        data = arguments.parse_args()
        data['password'] = create_password_hash(data['password'])
    
        if UserMoldel.find_by_login(data['login']):
            return {'message': f'The user {data["login"]} already exists'}
        
        new_user = UserMoldel(**data)
        print(new_user)
        new_user.save_user()
        return {'message': 'User created successfully.'}, 201 #Created
    
class UserLogin(Resource):

    @classmethod
    def post(cls):

        data = arguments.parse_args() 
        user = UserMoldel.find_by_login(data['login'])

        if user and verify_password(user.password, data['password']):
            access_token = create_access_token(identity=user.user_id)
            return {'access_token': access_token}, 200
        return{'message': 'The username or password is incorrect'}, 401


class UserLogout(Resource):

    @jwt_required()
    def post(self):

        jwt_id = get_jwt()['jti'] # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logget out successfuly!'}, 200




            


    
