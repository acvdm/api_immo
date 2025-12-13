from flask_restful import reqparse


# --- USER ---
def get_user_create_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help='Email is required')
    parser.add_argument('last_name', type=str, required=True, help='Last name is required')
    parser.add_argument('first_name', type=str, required=True, help='First name is required')
    parser.add_argument('birth_date', type=str, required=True, help='Birth date is required (YYYY-MM-DD)')
    return parser

def get_user_update_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=False)
    parser.add_argument('last_name', type=str, required=False)
    parser.add_argument('first_name', type=str, required=False)
    parser.add_argument('birth_date', type=str, required=False)
    return parser

def get_user_login_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help='Email is required')
    return parser


# --- PROPERTY ---
def get_property_create_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='Name is required')
    parser.add_argument('description', type=str, required=False)
    parser.add_argument('type', type=str, required=True, help='Type is required')
    parser.add_argument('city', type=str, required=True, help='City is required')
    parser.add_argument('price', type=int, required=False)
    parser.add_argument('size', type=int, required=True, help='Size is required')
    return parser

def get_property_update_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=False),
    parser.add_argument('description', type=str, required=False),
    parser.add_argument('type', type=str, required=False),
    parser.add_argument('city', type=str, required=False),
    parser.add_argument('price', type=str, required=False),
    parser.add_argument('size', type=int, required=False)
    return parser


# --- ROOM ---
def get_room_create_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('type', type=str, required=True, help='Type is required')
    parser.add_argument('size', type=int, required=True, help='size is required')
    return parser

def get_room_update_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('type', type=str, required=False)
    parser.add_argument('size', type=int, required=False)
    return parser