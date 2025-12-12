from app.models import Room
from flask_restful import Resource
from app.common.database import db
from app.common.parsers import get_room_create_parser, get_room_update_parser

# Attributs: id, property_id, type (bedroom/kitchen/etc.), size (m2)  
# Listre l'ensemble des pieces

# créer une pièce. `POST /properties/{property_id}/rooms`

# lister les pièces d'un bien. `GET /properties/{property_id}/rooms`

# lister les caractéristiques d'une pièce spécifique. `GET /rooms/{id}`

# modifier les caractéristiques d'une pièce. `PATCH /rooms/{id}` avec ownership check,

# supprimer une pièce. `DELETE /rooms/{id}` avec ownership check. 

class RoomsListResource(Resource):
    def get(self):
        rooms = Room.query.all()
        return {
            'rooms': [room.to_dict() for room in rooms]
        }, 200

    def post(self):
        parser = get_room_create_parser()
        args = parser.parse_args(strict=True)

        new_room = Room (
            property_id = args['property_id'],
            type = args['type'],
            size = args['size']
        )

        db.session.add(new_room)
        db.session.commit()

        return {
            'message': 'Room created successfully',
            'room': new_room.to_dict()
        }, 201
    
class RoomResource(Resource):
    def get(self, room_id):
        room = Room.query.get_or_404(room_id)
        return room.to_dict(), 200
    
    def patch(self, room_id):
        room = Room.query.get_or_404(room_id)

        parser = get_room_update_parser()
        args = parser.parse_args(strict=True)

        if args['type']:
            room.type = args['type']

        if args['size']:
            room.size = args['size']

        db.session.commit()

        return room.to_dict(), 200