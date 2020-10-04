from flask import request, jsonify
import uuid
import re
import speech_recognition as sr
import os

recognizer = sr.Recognizer()

LEOXIA_BASE_AUDIO_PATCH = "/tmp/leoxia/audio/"
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

    create_folder()
    path = LEOXIA_BASE_AUDIO_PATCH + '{name}'.format(name=uuid.uuid1())
    file.save(path)

    file_audio = sr.AudioFile(path)

    with file_audio as source:
        audio_text = recognizer.record(source)

    text = recognizer.recognize_google(audio_text, language='pt-BR')

    return process_text(text)


def command_by_text(username):
    text = request.json['text']
    return process_text(text)



def process_text(text):
    matches = re.finditer(regex, text, re.MULTILINE | re.IGNORECASE)
    for match in matches:
        command = match.group(1).upper()
        component = match.group(2).upper()
        action = prefix[match.group(1).upper()]
        return jsonify(
            {'Comando': '{}'.format(command), 'Componente': '{}'.format(component), 'Ação': '{}'.format(action)}), 200


def create_folder():
    try:
        os.makedirs(LEOXIA_BASE_AUDIO_PATCH)
    except OSError as e:
        print(e)
