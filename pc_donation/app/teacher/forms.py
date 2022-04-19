from flask_babel import lazy_gettext as _l
from wtforms import BooleanField, SubmitField

from app.common.form import ApprovalForm


class ConfirmStudentForm(ApprovalForm):
    approve = BooleanField(_l("Approve this student?"))
    submit = SubmitField(_l("Submit"))
