from flask import request, jsonify
from ..models.component_model import Component
from app import db
import RPi.GPIO as GPIO
import uuid
import re
import speech_recognition as sr
import os


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

recognizer = sr.Recognizer()

LEOXIA_BASE_AUDIO_PATCH = "/tmp/leoxia/audio/"
TURN_ON = 1
TURN_OFF = 0

prefix = {"LIGUE": TURN_ON, "LIGA": TURN_ON, "LIGAR": TURN_ON, "ACENDA": TURN_ON, "ACENDER": TURN_ON,
          "APAGAR": TURN_OFF, "APAGA": TURN_OFF, "DESLIGA": TURN_OFF, "DESLIGAR": TURN_OFF}

gpio_command_map = {TURN_OFF: GPIO.LOW, TURN_ON: GPIO.HIGH}
regex = r"({})".format('|'.join(prefix.keys())) + r"\s+\w{1,5}\s(.+$)"


def command_by_audio():
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


def command_by_text():
    text = request.json['text']
    return process_text(text)


def process_text(text):
    matches = re.finditer(regex, text, re.MULTILINE | re.IGNORECASE)
    for match in matches:
        command = match.group(1).upper()
        component_to_find = match.group(2).upper()
        action = prefix[match.group(1).upper()]
        print(f'Action: {action} - Component: {component_to_find} - Command {command}')
        component = Component.query.filter(Component.name == component_to_find).first()
        if component is None:
            return jsonify({'Message': 'Componente não encontrado'}), 404

        process_action(component, action)
        db.session.add(component)
        db.session.commit()
        return jsonify(
            {'Comando': '{}'.format(command), 'Componente': '{}'.format(component.name),
             'Ação': '{}'.format(action)}), 200


def command():
    id_to_find = request.json['id']
    action = request.json['action']
    if int(action) != TURN_ON and TURN_OFF:
        return jsonify({'Message': f'A ação a ser efetuada deve ser {TURN_ON} ou {TURN_OFF}'}), 400

    component = Component.query.filter(Component.id == id_to_find).first()
    if component is None:
        return jsonify({'Message': 'Componente não encontrado'}), 404
    process_action(component, action)
    db.session.add(component)
    db.session.commit()
    return jsonify(
        {'Componente': '{}'.format(component.name),
         'Ação': '{}'.format(action)}), 200


def process_action(component, action):
    for pin in component.pins:
        GPIO.setup(pin.name, GPIO.OUT)
        GPIO.output(pin.name, gpio_command_map[action])
        print(pin.to_dict())
    component.on = action


def create_folder():
    try:
        os.makedirs(LEOXIA_BASE_AUDIO_PATCH)
    except OSError as e:
        print(e)