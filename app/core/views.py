from flask import current_app as app
from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from werkzeug.local import LocalProxy

core = Blueprint('core', __name__, static_folder='static', template_folder='templates')
logger = LocalProxy(lambda: app.logger)

@core.before_request
def before_request_func():
    app.logger.name = 'core'

@core.route('/', methods=['GET'])
def index():
    fname = app.config['JEANNE_FILE']
    types_jeanne = app.config['TYPES_JEANNE']

    jeannes = []
    with open(fname, 'r') as fd:
        data = fd.readlines()
        for jeanne in data:
            jeannes.append(jeanne.strip().split('|'))
    return render_template('core/index.html', jeannes=jeannes, types_jeanne=types_jeanne)

@core.route('/ajouter-jeanne', methods=['POST'])
def ajouter():
    fname = app.config['JEANNE_FILE']

    data = request.form

    if 'jeanne-type' in data and 'lat' in data and 'lng' in data:
        try:
            jeanne_type = data['jeanne-type']
            lat = float(data['lat'])
            lng = float(data['lng'])
        except ValueError():
            return redirect(url_for('core.index'))
        else:
            with open(fname, 'a') as fd:
                fd.write(f"{jeanne_type}|{lat}|{lng}\n")
    return redirect(url_for('core.index'))
