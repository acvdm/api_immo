from flask import Flask
from flask_restful import Api
import os
from app.common.database import db



def create_app():
    app = Flask(__name__)

    # Connexion à PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql://realestate:password123@localhost:5432/real_estate_db'
    )

    # Bonne pratique, evite les warnings
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    api = Api(app)


    # Import et enregistrement des ressources
    from app.resources.users import UsersListResource, UserResource, UserPropertiesResource, UserLoginResource
    from app.resources.properties import PropertiesListResource, PropertyResource, PropertyRoomsResource
    from app.resources.rooms import RoomResource

    # routes
    api.add_resource(UsersListResource, '/users')
    api.add_resource(UserResource, '/users/<int:user_id>')
    api.add_resource(UserLoginResource, '/users/login')
    api.add_resource(UserPropertiesResource, '/users/<int:user_id>/properties')

    api.add_resource(PropertiesListResource, '/properties')
    api.add_resource(PropertyResource, '/properties/<int:property_id>')
    api.add_resource(PropertyRoomsResource, '/properties/<int:property_id>/rooms')

    api.add_resource(RoomResource, '/rooms/<int:room_id>')

    # route de test
    @app.route('/')
    def home():
        return {
            'message': 'Real Estate API',
            'status': 'running',
            'endpoints': {
                'users': '/users',
                'properties': '/properties',
                'rooms': '/rooms'
            }
        }

    return app