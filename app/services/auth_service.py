import datetime
from flask import request, jsonify
from ..models.user_model import User
from werkzeug.security import check_password_hash

import jwt


def auth():
    auth = request.authorization
    if not auth or not auth.password or not auth.username:
        return jsonify({'message': 'Você deve informar o usuário e a senha'}), 401

    user = User.query.filter(User.username == auth.username).first()

    if user is None:
        return jsonify({'message': 'Usuário inexistente'}), 404

    if check_password_hash(user.password, auth.password):
        return jwt.encode({'username': auth.username, 'exp': datetime.datetime.now() + datetime.timedelta(hours=20), 'group': user.group},
                          'LEOXIA@346615')
    else:
        return jsonify({'message': 'Usuário e senha inválido'}), 401

