from . import bp as api
from app.models import User
from app.blueprints.auth.auth import basic_auth, token_auth
from flask import g, make_response

@api.get('/token')
@basic_auth.login_required()
def get_token():
    user = g.current_user
    token = user.get_token()
    return make_response({"token": token}, 200)

