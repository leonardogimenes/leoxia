from app import app
from ..services import command_service
from ..configs import authorization


@app.route('/commands/audio', methods=['POST'])
@authorization.token_required
def command_by_audio():
    return command_service.command_by_audio()


@app.route('/commands/text', methods=['POST'])
@authorization.token_required
def command_by_text():
    return command_service.command_by_text()


@app.route('/commands', methods=['POST'])
@authorization.token_required
def command():
    return command_service.command()
