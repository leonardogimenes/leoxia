from functools import wraps
from flask import request, jsonify
import jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Autorização requerida'}), 401
        else:
            try:
                decode = jwt.decode(token, 'LEOXIA@346615')
                return f(decode.get('username'), *args, **kwargs)
            except Exception as e:
                print(e)
                return jsonify({'message': 'Token expirado'}), 401
    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Autorização requerida'}), 401
        else:
            try:
                decode = jwt.decode(token, 'LEOXIA@346615')
                group = decode.get('group')
                if group != 1:
                    return jsonify({'message': 'Você precisa ser um administrador'}), 403

                return f(*args, **kwargs)
            except Exception as e:
                print(e)
                return jsonify({'message': 'Token expirado'}), 401
    return decorated
