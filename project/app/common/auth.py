from flask import request

def get_current_user_id():
    user_id = request.headers.get('X-User-Id')

    if not user_id:
        print("No header user_id")
        return None
    
    return int(user_id)


