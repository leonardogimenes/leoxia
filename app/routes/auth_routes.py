from app import app
from ..services import auth_service


@app.route('/auth', methods=['POST'])
def auth():
    return auth_service.auth()
