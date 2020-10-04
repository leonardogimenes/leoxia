from flask import request, jsonify
import uuid
import re
import speech_recognition as sr

recognizer = sr.Recognizer()

TURN_ON = 1
TURN_OFF = 2

prefix = {"LIGUE": TURN_ON, "LIGA": TURN_ON, "LIGAR": TURN_ON, "ACENDA": TURN_ON, "ACENDER": TURN_ON,
          "APAGAR": TURN_OFF, "APAGA": TURN_OFF, "DESLIGA": TURN_OFF, "DESLIGAR": TURN_OFF}

regex = r"({})".format('|'.join(prefix.keys())) + r"\s+\w{1,5}\s(.+$)"


def command_by_audio(username):
    file = request.files['file']
    mime_type = file.content_type

    if mime_type != 'audio/wave':
        return jsonify({'message': 'O arquivo enviado é invalido'}), 400

    path = '/tmp/leoxia/audio/{name}'.format(name=uuid.uuid1())
    file.save(path)

    file_audio = sr.AudioFile(path)

    with file_audio as source:
        audio_text = recognizer.record(source)

    text = recognizer.recognize_google(audio_text, language='pt-BR')
    process_text(text)

    return jsonify('Sucesso'), 200


def command_by_text(username):
    text = request.json['text']
    process_text(text)
    return jsonify('Sucesso'), 200


def process_text(text):
    matches = re.finditer(regex, text, re.MULTILINE | re.IGNORECASE)
    for match in matches:
        print("Comando: {}".format(match.group(1)))
        print("Componente: {}".format(match.group(2)))
        print(prefix[match.group(1).upper()])
