from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

db = SQLAlchemy()

def create_app(config_object=None):
    app = Flask(__name__)

    # Par défaut : modifier si nécessaire (ne pas hardcoder en production)
    app.config.setdefault(
        'SQLALCHEMY_DATABASE_URI',
        'postgresql://realestate:password123@db:5432/real_estate_db'
    )
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    if config_object:
        app.config.from_object(config_object)

    db.init_app(app)

    from . import models 

    api = Api(app)

    from .routes.users import Users
    api.add_resource(Users, '/users')

    # route de test
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