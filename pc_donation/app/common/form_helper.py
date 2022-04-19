import flask
from flask_babel import _

from app.model.models import Region, EquipmentType


def populate_form_regions(form):
#    form.region_id.choices = [(-1, _("Please select"))] + [(s.id, _(s.name))
#                                                           for s in flask.g.session.query(Region).all()]
     form.region_id.choices = [(s.id, _(s.name)) for s in flask.g.session.query(Region).all()]


def populate_form_equipment_types(form):
    form.equipment_type_id.choices = [(s.id, _(s.name)) for s in flask.g.session.query(EquipmentType).all()]
