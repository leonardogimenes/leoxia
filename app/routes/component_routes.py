from app import app
from ..configs import authorization
from ..services import component_service


@app.route('/components', methods=['GET'])
# @authorization.token_required
def list_components():
    return component_service.list_components()


@app.route('/components', methods=['POST'])
# @authorization.admin_token_required
def create_component():
    return component_service.create_component()


@app.route('/components/<component_id>', methods=['DELETE'])
# @authorization.admin_token_required
def delete_component(component_id):
    return component_service.delete_component(component_id)


@app.route('/components/<component_id>/pins', methods=['GET'])
# @authorization.admin_token_required
def list_pins_from_component(component_id):
    return component_service.list_pins_from_component(component_id)


@app.route('/components/<component_id>/pins/<pin_id>', methods=['DELETE'])
def delete_pin_from_component(component_id, pin_id):
    return component_service.delete_pin_from_component(component_id, pin_id)


@app.route('/components/<component_id>/pins', methods=['POST'])
def create_pin_in_component(component_id):
    return component_service.create_pin_in_component(component_id)

