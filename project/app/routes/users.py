from flask import request
from flask_restful import Resource, Api, reqparse
from app import db
from app.models import User
 

# créer un utilisateur. POST /users
user_create_parser = reqparse.RequestParser()
user_create_parser.add_argument('email', type=str, required=True, help='Email is required')
user_create_parser.add_argument('last_name', type=str, required=True, help='Last name is required')
user_create_parser.add_argument('first_name', type=str, required=True, help='First name is required')
user_create_parser.add_argument('birth_date', type=str, required=True, help='Birth date is required (YYYY-MM-DD)')

class Users(Resource):
    # lister l'ensemble des utilisateurs
    def get(self):
        users = User.query.all()
        return {
            'users': [user.to_dict() for user in users]
        }, 200

    # Créer un nouvel utilisateur
    def post(self):
        args = user_create_parser.parse_args()

        # Vérifier si l'email existe déjà
        if User.query.filter_by(email=args['email']).first():
            return {'error': 'Email already exists'}, 409

        # Créer l'utilisateur
        new_user = User(
            email=args['email'],
            last_name=args['last_name'],
            first_name=args['first_name'],
            birth_date=birth_date
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return {
            'message': 'User created successfully',
            'user': new_user.to_dict()
        }, 201


# Fonction pour enregistrer les routes
#def register_routes(api):
 #   api.add_resource(Users, '/users')

# lister les infos personnelles d un utilisateur. GET /users/{id}

# modifier ses infos personnelles. PATCH /users/{id} avec ownership check

# lister les biens d un utilisateur. GET /users/{id}/properties

# authentification du user. POST /users/login  