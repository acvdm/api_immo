from flask_restful import Resource
from app.common.database import db
from app.models import User, Property
from datetime import datetime
from app.common.parsers import get_user_create_parser, get_user_update_parser, get_user_login_parser


class UsersListResource(Resource):
    # lister l'ensemble des utilisateurs
    def get(self):
        users = User.query.all()
        return {
            'users': [user.to_dict() for user in users]
        }, 200

    # Créer un nouvel utilisateur
    def post(self):
        # reqparse() retourne un dictionnaire 
        # Calling parse_args with strict=True ensures that an error is thrown 
        # if the request includes arguments your parser does not define.
        parser = get_user_create_parser()
        args = parser.parse_args(strict=True)

        # Vérifier si l'email existe déjà
        if User.query.filter_by(email=args['email']).first():
            return {
                'error': 'Email already exists'
            }, 409

        birth_date = datetime.strptime(args['birth_date'], '%Y-%m-%d').date()

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


# lister les infos personnelles d'un utilisateur. GET /users/{id}
class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user.to_dict(), 200
    
    def patch(self, user_id):
        user = User.query.get_or_404(user_id)

        parser = get_user_update_parser()
        args = parser.parse_args(strict=True)

        if args['email']: 
            user.email = args['email']
        if args['last_name']:
            user.last_name = args['last_name']
        if args['first_name']:
            user.first_name = args['first_name']
        if args['birth_date']:
            user.birth_date = datetime.strptime(args['birth_date'], '%Y-%m-%d').date()

        db.session.commit()

        return user.to_dict(), 200

# lister les biens d'un utilisateur. GET /users/{id}/properties
class UserPropertiesResource(Resource):
    def get(self, user_id):
        User.query.get_or_404(user_id)

        query = Property.query.filter(Property.owner_id == user_id)
        properties = query.all()
        return {
            "properties": [property.to_dict() for property in properties]
        }, 200

# authentification du user. POST /users/login 
# Renvoie le user_id qui devra ensuite être mis dans X-User-Id: {user_id} pour toutes les requêtes avec ownership
class UserLoginResource(Resource):
    def post(self):
        parser = get_user_login_parser()
        args = parser.parse_args()

        user = User.query.filter_by(email=args['email']).first()

        if not user:
            return {'message': 'User not found'}, 404
        
        return {
            'message': 'Login successful',
            'user_id': user.id,
            'user': user.to_dict()
        }, 200