from datetime import datetime

from flask_babel import lazy_gettext as _l
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, \
    HiddenField

from app.common.form import CommonForm, DateTimeField

now = datetime.now()


class AppointmentForm(CommonForm):
    id = HiddenField(_l("id"), render_kw={"readonly": True})
    first_name = StringField(_l("First Name"), render_kw={"readonly": True},
                             validators=CommonForm.NAME_VALIDATORS)
    last_name = StringField(_l("Last Name"), render_kw={"readonly": True},
                            validators=CommonForm.NAME_VALIDATORS)
    address = StringField(_l("Address"), render_kw={"readonly": True})
    title = TextAreaField(_l("Problem"), render_kw={"readonly": True}, validators=CommonForm.TITTLE_VALIDATORS)
    description = TextAreaField(_l("Description Problem"), render_kw={"readonly": True},
                                validators=CommonForm.DESCRIPTION_VALIDATORS)
    date_time = DateTimeField(_l("Repair time"), validators=CommonForm.MEET_UP_DATE_TIME_VALIDATORS)
    submit = SubmitField(_l("Submit"))


class StoryPermissionForm(CommonForm):
    id = HiddenField(_l("id"), render_kw={"readonly": True})
    student_name = StringField(_l("Student Name"), render_kw={"readonly": True})
    title = TextAreaField(_l("Title"), render_kw={"readonly": True})
    story = TextAreaField(_l("Story"), render_kw={"readonly": True})
    item_name = StringField(_l("Item Name"), render_kw={"readonly": True})
    permission = BooleanField(_l("Permission"))
    submit = SubmitField(_l("Submit"))
