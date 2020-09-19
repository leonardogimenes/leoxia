from app import app
from ..services import users_service
from ..configs import authorization


@app.route('/users', methods=['GET'])
@authorization.admin_token_required
def find_users():
    return users_service.find_users()


@app.route('/users', methods=['POST'])
@authorization.admin_token_required
def create_user():
    return users_service.create_user()


@app.route('/users/<user_id>/change-password', methods=['PATCH'])
def change_password(user_id):
    return users_service.change_user_password(user_id)


@app.route('/users/<user_id>', methods=['DELETE'])
@authorization.admin_token_required
def delete_user(user_id):
    return users_service.delete_user(user_id)
