from app.models.User import User
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:

    def __init__(self, db):
        self.users = db.users

    def check_complete_user(self, user_data):
        if not user_data or not 'username' in user_data or not 'password' in user_data:
            return {'error': 'The request payload is incomplete.'}, 400
        else:
            return User(user_data["username"], user_data["first_name"], user_data["last_name"], user_data["password"])
        
    def check_if_registered(self, user):
        print(self.users.count_documents({}))
        if self.users.find_one({'username': user.username}):
            return True
        else: 
            return False
        
    def add_user(self, user):
        hashed_password = generate_password_hash(user.password)
        user.password = hashed_password
        self.users.insert_one(user.to_dict())
        return {'message': 'User registered successfully.'}, 201
    
    def get_user(self, username):
        user_data = self.users.find_one({'username': username})
        if user_data:
            return User(
                username=user_data['username'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                password=user_data['password']
            )
        else:
            return None
        
    def verify_user(self, username, password):
        user = self.get_user(username)
        if user and check_password_hash(user.password, password):
            return user
        else:
            return None
        