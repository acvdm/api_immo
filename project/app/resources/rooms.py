from app.models import Room, Property
from flask_restful import Resource
from app.common.database import db
from app.common.parsers import get_room_update_parser
from app.common.auth import get_current_user_id


class RoomResource(Resource):
    def get(self, room_id):
        room = Room.query.get_or_404(room_id)
        return room.to_dict(), 200

    
    def patch(self, room_id):
        user_id = get_current_user_id()
        if user_id is None:
            return {'error': 'X-User-Id header is required'}, 401
        
        room = Room.query.get_or_404(room_id)

        property = Property.query.get_or_404(room.property_id)
        if property.owner_id != user_id:
            return {'error': 'Forbidden'}, 403

        parser = get_room_update_parser()
        args = parser.parse_args(strict=True)

        if args['type']:
            room.type = args['type']

        if args['size']:
            room.size = args['size']

        db.session.commit()

        return room.to_dict(), 200
    
    def delete(self, room_id):
        user_id = get_current_user_id()
        if user_id is None:
            return {'error': 'X-User-Id header is required'}, 401
        
        room = Room.query.get_or_404(room_id)

        property = Property.query.get_or_404(room.property_id)
        if property.owner_id != user_id:
            return {'error': 'Forbidden'}, 403
        
        db.session.delete(room)
        db.session.commit()

        return '', 204