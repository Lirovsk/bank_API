from flask_jwt_extended import jwt_required, get_jwt_identity
from ..app.extension import jwt
from ..models import Player


@jwt.user_identity_loader
def user_identity_lookup(player):
    return str(player.id)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Player.query.filter_by(id=identity).one_or_none()
