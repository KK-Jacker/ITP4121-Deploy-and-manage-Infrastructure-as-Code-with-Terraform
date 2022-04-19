from datetime import datetime

from flask_babel import lazy_gettext as _l
from wtforms import StringField, BooleanField, SubmitField, FloatField
from wtforms.fields.html5 import DateField

from app.common.form import CommonForm, ApprovalForm


class ConfirmTeacherForm(ApprovalForm):
    office_phone_number = StringField(_l("Office Phone Number", validators=CommonForm.OFFICE_PHONE_VALIDATORS),
                                      render_kw={"readonly": True})
    approve = BooleanField(_l("Approve this teacher?"))
    submit = SubmitField(_l("Save"))


class VerifyReceiptForm(CommonForm):
    receipt_date = DateField(_l("Date"), default=datetime.now())
    receipt_total = FloatField(_l("Total"))
    receipt_merchant_name = StringField(_l("Merchant Name"), validators=CommonForm.TITTLE_VALIDATORS)
    receipt_reject_reason = StringField(_l("Reject Reason"), validators=CommonForm.OPTIONAL_MESSAGE_VALIDATORS)
    approve = BooleanField(_l("Verify this Donation Receipt?"), render_kw={'class': 'radiocheckbox'})
    reject = BooleanField(_l("Reject this Donation Receipt?"), render_kw={'class': 'radiocheckbox'})
    submit = SubmitField(_l("Save"))
