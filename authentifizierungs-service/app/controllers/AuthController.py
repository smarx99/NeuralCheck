from app.services.AuthService import AuthService
from app.models.User import User
import jwt

class AuthController: 
    def __init__(self, db):
        self.auth_service = AuthService(db)

    # Register user
    def register_user(self, user_data):
        try:
            # Check if user data is complete
            result = self.auth_service.check_complete_user(user_data)
            if isinstance(result, tuple):  
                return result[0], result[1]
            
            user = result  
            
            # Check if user alreadey exists
            if self.auth_service.check_if_registered(user):
                return {'error': 'Username already exists.'}, 400

            # Otherwise add user
            response, status = self.auth_service.add_user(user)
            return response, status
        except Exception as e:
            print("An error occured while registering the user: ",e)
            return {'error': 'Error while registering the user'}, 400

    # Login user
    def login_user(self, user_data):
        try:
            # Check if username and password is correct
            user = self.auth_service.verify_user(user_data['username'], user_data['password'])
            return user
        except Exception as e:
            print("An error occured while logging in the user: ",e)
            return {'error': 'Error while logging in the user'}, 400

    # Get user data  
    def get_user(self, use_data):
        try:
            user = self.auth_service.get_user(use_data['username'])
            return user
        except Exception as e:
            print("An error occured while getting the user: ",e)
            return {'error': 'Error while getting the user'}, 400

    # Decode token to check if expired or invalid   
    def validate_token(self, token, key):
        try:
            decoded = jwt.decode(token, key, algorithms=["HS256"])
            return decoded
        except jwt.ExpiredSignatureError:
            return {'error': 'Token has expired'}
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token'}


