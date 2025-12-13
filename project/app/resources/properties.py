from flask_restful import Resource
from flask import request
from app.common.database import db
from app.models import Property, Room
from app.common.parsers import get_property_create_parser, get_property_update_parser, get_room_create_parser
from app.common.auth import get_current_user_id 


class PropertiesListResource(Resource):
    # Lister tous les biens de la plateforme 
    def get(self):
        
        city = request.args.get("city", None, type=str)
        print("city param:", repr(city))
        query = Property.query

        if city:
            query = query.filter_by(city=city)

        properties = query.all()
        return {
            'properties': [property.to_dict() for property in properties]
        }, 200


    # créer un bien. `POST /properties` user_id requis
    def post(self):
        user_id = get_current_user_id()
        if user_id is None:
            return {'error': 'X-User-Id header is required'}, 401
        
        parser = get_property_create_parser()
        args = parser.parse_args(strict=True)

        new_property = Property(
            owner_id = user_id,
            name = args['name'],
            description = args['description'],
            type = args['type'],
            city = args['city'],
            price = args['price'],
            size = args['size']
        )

        db.session.add(new_property)
        db.session.commit()

        return {
            'message': 'Property created successfully',
            'property': new_property.to_dict()
        }, 201



class PropertyResource(Resource):
    def get(self, property_id):
        property = Property.query.get_or_404(property_id)
        return property.to_dict(), 200
    
    # modifier les caractéristiques d'un bien. `PATCH /properties/{id} avec` ownership check
    def patch(self, property_id):
        user_id = get_current_user_id()
        if user_id is None:
            return {'error': 'X-User-Id header required'}, 401

        property = Property.query.get_or_404(property_id)

        if property.owner_id != user_id:
            return {'error': 'Forbidden'}, 403
        
        parser = get_property_update_parser()
        args = parser.parse_args(strict=True)

        if args['name']:
            property.name = args['name']
        if args['description']:
            property.description = args['description']
        if args['type']:
            property.type = args['type']
        if args['city']:
            property.city = args['city']
        if args['price']:
            property.price = args['price']
        if args['size']:
            property.size = args['size']

        db.session.commit()

        return property.to_dict(), 200
    
    def delete(self, property_id):
        user_id = get_current_user_id()
        if user_id is None:
            return {'error': 'X-User-Id is required'}, 401
        
        property = Property.query.get_or_404(property_id)

        if property.owner_id != user_id:
            return {'error': 'Forbidden'}, 403
        
        db.session.delete(property)
        db.session.commit()
        
        return '', 204
        



# lister les rooms d'une property. GET /properties/{id}/rooms
class PropertyRoomsResource(Resource):
    def get(self, property_id):
        Property.query.get_or_404(property_id)

        query = Room.query.filter(Room.property_id == property_id)
        Rooms = query.all()
        return {
            "properties": [room.to_dict() for room in Rooms]
        }, 200
    
    def post(self, property_id):
        user_id = get_current_user_id()
        if user_id is None:
            return {'error': 'X-User-Id header is required'}, 401
        
        property = Property.query.get_or_404(property_id)

        if property.owner_id != user_id:
            return {'error': 'Forbidden'}, 403
        
        parser = get_room_create_parser()
        args = parser.parse_args(strict=True)

        new_room = Room (
            property_id = property_id,
            type = args['type'],
            size = args['size']
        )

        db.session.add(new_room)
        db.session.commit()

        return {
            'message': 'Room created successfully',
            'room': new_room.to_dict()
        }, 201


# supprimer un bien. `DELETE /properties/{id}` avec ownership check.
