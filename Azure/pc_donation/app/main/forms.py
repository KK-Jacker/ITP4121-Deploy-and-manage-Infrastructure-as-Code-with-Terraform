from flask_babel import lazy_gettext as _l
from wtforms import StringField, SubmitField, \
    SelectField

from app.common.form import CommonForm


class EditProfileForm(CommonForm):
    # TODO: username cannot be changed by hack
    # username = StringField(_l("Username"), validators=CommonForm.USERNAME_VALIDATORS, render_kw={"readonly": True})
    first_name = StringField(_l("First Name"), validators=CommonForm.NAME_VALIDATORS)
    last_name = StringField(_l("Last Name"), validators=CommonForm.NAME_VALIDATORS)
    region_id = SelectField(_l("Region"), validators=CommonForm.SELECT_VALIDATORS, coerce=int)
    phone_number = StringField(_l("Phone Number"),
                               validators=CommonForm.PHONE_VALIDATORS, render_kw={"placeholder": _l("phone_require")})
    submit = SubmitField(_l("Submit"))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
