from functools import wraps
from flask import abort, request, g
from werkzeug.security import check_password_hash
from .models import User


def authorization_required_api(func):
    @wraps(func)
    def check_request(*args, **kwargs):
        auth = request.authorization
        if not auth:
            abort(401)
        username, password = auth.get('username'), auth.get('password')
        if not (username and password):
            abort(401)
        api_user = g.db.query(User).filter_by(username=username,
                                              user_type='api').first()
        if not (api_user and check_password_hash(api_user.password, password)):
            abort(401)
        return func(*args, **kwargs)
    return check_request
