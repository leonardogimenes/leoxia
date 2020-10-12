from flask import request, jsonify
from ..models.component_model import Component
from ..models.pin_model import Pin
from app import db


def create_component():
    name = request.json['name']
    description = request.json['description']
    on = request.json['on']
    pins = request.json['pins']
    component = Component(name=name, description=description, on=on)
    for pin in pins:
        name = pin['name']
        pin_model = Pin(name=name, component=component)
        component.pins.append(pin_model)
    try:
        db.session.add(component)
        db.session.commit()
    except Exception:
        return jsonify({'message': 'Erro ao criar componente'}), 400

    return jsonify({'message': 'Componente criado com sucesso'}), 201


def list_components():
    components = Component.query.all()
    results = [component.to_dict() for component in components]
    return jsonify(results), 200


def delete_component(component_id):
    component = get_component_by_id(component_id)

    if component is None:
        return jsonify({'message': 'Componente inexistente'}), 404

    db.session.delete(component)
    db.session.commit()

    return jsonify({'message': 'Componente deletado'}), 200


def list_pins_from_component(component_id):
    component = get_component_by_id(component_id)
    if component is None:
        return jsonify({'message': 'Componente inexistente'}), 404

    results = [pin.to_dict() for pin in component.pins]
    return jsonify(results), 200


def delete_pin_from_component(component_id, pin_id):
    component = get_component_by_id(component_id)
    if component is None:
        return jsonify({'message': 'Componente inexistente'}), 404

    for pin in component.pins:
        if pin.id == int(pin_id):
            db.session.delete(pin)
            db.session.commit()
            return jsonify({'message': 'Pino deletado'}), 200

    return jsonify({'message': 'Pino não encontrado'}), 404


def create_pin_in_component(component_id):
    component = get_component_by_id(component_id)
    if component is None:
        return jsonify({'message': 'Componente inexistente'}), 404

    name = request.json['name']
    pin_model = Pin(name=name, component=component)
    try:
        component.pins.append(pin_model)
    except Exception:
        return jsonify({'message': 'Pino já existe'}), 400

    try:
        db.session.add(component)
        db.session.commit()
    except Exception:
        return jsonify({'message': 'Erro ao criar pino no componente'}), 400

    return jsonify({'message': 'Pino criado com sucesso'}), 201


def get_component_by_id(component_id):
    return Component.query.filter(Component.id == component_id).first()
