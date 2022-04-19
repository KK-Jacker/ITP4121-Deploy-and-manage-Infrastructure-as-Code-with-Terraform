from flask_babel import lazy_gettext as _l
from flask_wtf.file import FileField
from wtforms import SubmitField, SelectField, StringField
from wtforms.validators import DataRequired

from app.common.form import CommonForm, DateTimeField


class DonateEquipmentForm(CommonForm):
    equipment_type_id = SelectField(_l("Please enter your equipment type"), validators=[DataRequired()], coerce=int)
    # TODO: not required
    description = StringField(_l("Please enter your description"), validators=CommonForm.MESSAGE_VALIDATORS)
    equipment_photo = FileField(_l("Please upload your equipment photo"),
                                validators=CommonForm.NO_FACE_IMAGE_VALIDATORS)
    receipt_photo = FileField(_l("If possible, please upload your receipt photo for our record."),
                              validators=CommonForm.RECEIPT_IMAGE_VALIDATORS)
    submit = SubmitField(_l("Add"))


class SelectedItemForm(CommonForm):
    item = SelectField(_l("Please enter your Item Object"), validators=[DataRequired()], render_kw={"readonly": True})


class DonateConfirmForm(CommonForm):
    date_time = DateTimeField(_l("Meetup time"), validators=CommonForm.MEET_UP_DATE_TIME_VALIDATORS)
    submit = SubmitField(_l("Confirm Your Donation."))
