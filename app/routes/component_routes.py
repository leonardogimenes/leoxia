from app import app
from ..configs import authorization


@app.route('/')
@authorization.token_required
def hello_world2():
    return 'Hello World!'
