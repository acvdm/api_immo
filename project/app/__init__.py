from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Par défaut : modifier si nécessaire (ne pas hardcoder en production)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql://realestate:password123@localhost:5432/real_estate_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')


    db.init_app(app)
    api = Api(app)

    from app.models import User 

    from app.routes.users import UsersListResource, UserResource, UserLoginResource
    api.add_resource(UsersListResource, '/users')
    api.add_resource(UserResource, '/users/<int:user_id>')
    api.add_resource(UserLoginResource, '/users/login')

    #route de test
    @app.route('/')
    def home():
        return {
            'message': 'Real Estate API',
            'status': 'running',
            'endpoints': {
                'users': '/users',
            }
        }

    return app