from flask import current_app as app
from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from werkzeug.local import LocalProxy

from .model import Jeanne, JeanneType, JeanneTypeForm

core = Blueprint('core', __name__, static_folder='static', template_folder='templates')
logger = LocalProxy(lambda: app.logger)

@core.before_request
def before_request_func():
    app.logger.name = 'core'

@core.route('/', methods=['GET'])
def index():
    types_jeanne = {jeanne.jeanne_type: (jeanne.jeanne_name, jeanne.jeanne_color) for jeanne in JeanneType.objects()}

    jeannes = Jeanne.objects()

    return render_template('core/index.html', jeannes=jeannes, types_jeanne=types_jeanne)

@core.route('/ajouter-jeanne', methods=['POST'])
def ajouter():
    data = request.form

    if 'jeanne_type' in data and 'lat' in data and 'lng' in data:
        try:
            jeanne_type = data['jeanne_type']
            lat = float(data['lat'])
            lng = float(data['lng'])
        except ValueError():
            return redirect(url_for('core.index'))
        else:
            obj = Jeanne(jeanne_type=jeanne_type, lat=lat, lng=lng)
            obj.save()

    return redirect(url_for('core.index'))

@core.route('/jeannes', methods=['GET'])
def types_list():
    types = JeanneType.objects()

    return render_template('core/types_list.html', types=types)

@core.route('/jeannes/new', methods=['GET', 'POST'])
def types_insert():
    obj = JeanneType()
    form = JeanneTypeForm(obj=obj)

    if form.validate_on_submit():
        form.populate_obj(obj)
        obj.save()
        return redirect(url_for("core.types_list"))

    return render_template('core/types_insert_edit.html', form=form)

@core.route('/jeannes/<jeanne_type>', methods=['GET', 'POST'])
def types_edit(jeanne_type):
    obj = JeanneType.objects.get_or_404(jeanne_type=jeanne_type)
    form = JeanneTypeForm(obj=obj)

    if form.validate_on_submit():
        form.populate_obj(obj)
        obj.save()
        return redirect(url_for("core.types_list"))

    return render_template('core/types_insert_edit.html', form=form)
