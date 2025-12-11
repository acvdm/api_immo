from flask_restful import Resource
from flask import request
from app.common.database import db
from app.models import Property
from datetime import datetime
from app.common.parsers import get_property_create_parser, get_property_update_parser


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


    # créer un bien. `POST /properties` user_id requis TODO,
    def post(self):
        parser = get_property_create_parser()
        args = parser.parse_args(strict=True)

        new_property = Property(
            owner_id = args['owner_id'],
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
    
    # modifier les caractéristiques d'un bien. `PATCH /properties/{id} avec` ownership check, TODO
    def patch(self, property_id):
        property = Property.query.get_or_404(property_id)
        print("property_id ${property_id}")

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


# supprimer un bien. `DELETE /properties/{id}` avec ownership check.
