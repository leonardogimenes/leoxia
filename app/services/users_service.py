from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user_model import User, db


def create_user():
    username = request.json['username']
    password = request.json['password']
    user = User(username=username, password=generate_password_hash(password), group=0)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception:
        return jsonify({'message': 'Erro ao criar usuário'}), 400

    return jsonify({'message': 'Usuário criado com sucesso'}), 201


def find_users():
    users = User.query.all()
    results = [user.to_dict() for user in users]
    return jsonify(results), 200


def change_user_password(user_id):
    password = request.json['password']
    new_password = request.json['new_password']
    user = get_user_by_id(user_id)

    if user is None:
        return jsonify({'message': 'Usuário inexistente'}), 404

    if not check_password_hash(user.password, password):
        return jsonify({'message': 'Senha atual incorreta'}), 401

    user.password = generate_password_hash(new_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Senha alterada com sucesso'}), 200


def delete_user(user_id):
    user = get_user_by_id(user_id)

    if user is None:
        return jsonify({'message': 'Usuário inexistente'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'Usuario deletado'}), 200


def get_user_by_request_username():
    username = request.json['username']
    return User.query.filter(User.username == username).first()


def get_user_by_id(user_id):
    return User.query.filter(User.id == user_id).first()
