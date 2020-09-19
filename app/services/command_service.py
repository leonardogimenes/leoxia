from flask import request, jsonify
import uuid


def command_by_audio(username):
    file = request.files['file']
    mime_type = file.content_type

    if mime_type != 'audio/mpeg':
        return jsonify({'message': 'O arquivo enviado é invalido'}), 400

    path = '/tmp/leoxia/audio/{name}'.format(name=uuid.uuid1())
    file.save(path)

    # TODO-> Implementar transcrissor de audio GOOGLE

    process_text('Audio endpoint ' + username)
    return jsonify('Sucesso'), 200


def command_by_text(username):
    text = request.json['text']
    process_text(text + ' ' + username)
    return jsonify('Sucesso'), 200


def process_text(text):
    print('Text: {}', text)
