from flask import current_app as app
from flask_mongoengine import Document
from flask_mongoengine.wtf import model_form
from mongoengine import StringField, FloatField, ReferenceField, DateTimeField
from datetime import datetime

class JeanneType(Document):
    jeanne_type = StringField(required=True, max_length=256, primary_key=True)
    jeanne_name = StringField(required=True, max_length=256)
    jeanne_color = StringField(required=True, max_length=256)

JeanneTypeForm = model_form(JeanneType)

class Jeanne(Document):
    jeanne_type = ReferenceField(JeanneType)
    lat = FloatField()
    lng = FloatField()
    created_at = DateTimeField(default=datetime.now())
