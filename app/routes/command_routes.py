from app import app
from ..services import command_service
from ..configs import authorization


@app.route('/commands/audio', methods=['POST'])
@authorization.token_required
def command_by_audio(username):
    return command_service.command_by_audio(username)


@app.route('/commands/text', methods=['POST'])
@authorization.token_required
def command_by_text(username):
    return command_service.command_by_text(username)
