from flask_babel import lazy_gettext as _l
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, \
    TextAreaField, HiddenField, SelectField
from wtforms.validators import DataRequired

from app.common.form import CommonForm


class StudentStoryForm(CommonForm):
    id = HiddenField()
    title = StringField(_l("Please enter your title of your story to donor"), validators=CommonForm.TITTLE_VALIDATORS)
    content = TextAreaField(
        _l("Please elaborate your story about your life to make the donor willing to donate equipment to you"),
        validators=CommonForm.STORY_VALIDATORS)
    story_photo = FileField(_l("Please Upload a photo about your life the photo will show to the donor"),
                            validators=CommonForm.NO_FACE_IMAGE_VALIDATORS)
    submit = SubmitField(_l("Submit"))


class ViewStudentStoryForm(CommonForm):
    id = HiddenField(render_kw={"readonly": True})
    title = StringField(_l("Please enter your title of your story to donor"), validators=CommonForm.TITTLE_VALIDATORS,
                        render_kw={"readonly": True})
    content = TextAreaField(
        _l("Please elaborate your story about your life to make the donor willing to donate equipment to you"),
        validators=CommonForm.STORY_VALIDATORS, render_kw={"readonly": True})


class EquipmentApplicationForm(CommonForm):
    equipment_type_id = SelectField(_l("Please choose your equipment type"), validators=[DataRequired()], coerce=int)
    submit = SubmitField(_l("Apply Equipment"))


class EquipmentApplicationLocationForm(CommonForm):
    latitude = HiddenField(validators=CommonForm.LATITUDE_VALIDATORS)
    longitude = HiddenField(validators=CommonForm.LONGITUDE_VALIDATORS)
    submit = SubmitField(_l("Submit"))


class ThankToDonorForm(CommonForm):
    thanks_message = TextAreaField(_l("Thanks Message To Your Donor"),
                                   validators=CommonForm.THANKS_VALIDATORS)
    thanks_photo = FileField(_l("Please upload a photo with your donor"),
                             validators=CommonForm.IMAGE_VALIDATORS)
    submit = SubmitField(_l("Submit"))


class ThankToVolunteerForm(CommonForm):
    thanks_message = TextAreaField(_l("Thanks Message To Your Volunteer"),
                                   validators=CommonForm.THANKS_VALIDATORS)
    thanks_photo = FileField(_l("Please upload a photo with your volunteer"),
                             validators=CommonForm.IMAGE_VALIDATORS)
    submit = SubmitField(_l("Submit"))


class RepairApplicationForm(CommonForm):
    id = HiddenField()
    title = StringField(_l("Title"), validators=CommonForm.TITTLE_VALIDATORS)
    description = TextAreaField(
        _l("Describe your technical problem."),
        validators=CommonForm.DESCRIPTION_VALIDATORS)
    equipment_photo = FileField(_l("Upload the device photo."),
                                validators=CommonForm.NO_FACE_IMAGE_VALIDATORS)
    address = StringField(_l("Detail Address", validators=[CommonForm.ModerateText()]))
    latitude = HiddenField(validators=CommonForm.LATITUDE_VALIDATORS)
    longitude = HiddenField(validators=CommonForm.LONGITUDE_VALIDATORS)
    submit = SubmitField(_l("Submit"))
