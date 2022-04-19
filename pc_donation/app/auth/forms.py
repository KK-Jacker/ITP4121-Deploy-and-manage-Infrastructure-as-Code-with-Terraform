from flask_babel import lazy_gettext as _l
from flask_wtf import RecaptchaField
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField
from wtforms.fields.html5 import EmailField

from app.common.form import CommonForm
from app.model.status_enum import GenderEnum
from config import RecaptchaConfig as Recaptcha


class LoginForm(CommonForm):
    username = StringField(_l("Username or email"), validators=CommonForm.LOGIN_VALIDATORS)
    password = PasswordField(_l("Password"), validators=CommonForm.PASSWORD_VALIDATORS)
    remember_me = BooleanField(_l("Remember Me"))
    if Recaptcha.ENABLE:
        recaptcha = RecaptchaField()
    submit = SubmitField(_l("Sign In"))


class ResentConfirmationEmailForm(CommonForm):
    if Recaptcha.ENABLE:
        recaptcha = RecaptchaField()
    submit = SubmitField(_l("Resend Email Conformation Email."))


class RegistrationForm(CommonForm):
    username = StringField(_l("Username"),
                           validators=CommonForm.NEW_USERNAME_VALIDATORS)
    first_name = StringField(_l("First Name (ENG)"),
                             validators=CommonForm.NAME_VALIDATORS)
    last_name = StringField(_l("Last Name (ENG)"),
                            validators=CommonForm.NAME_VALIDATORS)
    first_name_zh_hant = StringField(_l("First Name (Chinese)"),
                                     validators=CommonForm.CHI_NAME_VALIDATORS)
    last_name_zh_hant = StringField(_l("Last Name (Chinese)"),
                                    validators=CommonForm.CHI_NAME_VALIDATORS)

    region_id = SelectField(_l("Region"), validators=CommonForm.SELECT_VALIDATORS, coerce=int)

    password = PasswordField(_l("Password"),
                             validators=CommonForm.PASSWORD_VALIDATORS)
    password2 = PasswordField(_l("Repeat Password"),
                              validators=CommonForm.CONFIRM_PASSWORD_VALIDATORS)
    phone_number = StringField(_l("Phone Number"),
                               validators=CommonForm.PHONE_VALIDATORS,
                               render_kw={"placeholder": _l("phone_require")})
    user_photo = FileField(_l("Your Photo"),
                           validators=CommonForm.IMAGE_VALIDATORS)

    short_style = {'style': 'width:50%;'}

    gender = SelectField(_l("Gender"),
                         choices=GenderEnum.choices(),
                         coerce=GenderEnum.coerce,
                         validators=CommonForm.SELECT_VALIDATORS,
                         render_kw=short_style,)

    dateOfBirth = StringField(_l("Birth (yyyy-mm-dd)"),
                              validators=CommonForm.BIRTH_VALIDATORS,
                              render_kw=short_style)


class VolunteerOrDonorRegistrationForm(RegistrationForm):
    email = EmailField(_l("Email"), validators=CommonForm.NEW_EMAIL_VALIDATORS)


class StudentOrTeacherRegistrationForm(RegistrationForm):
    pass


class VolunteerForm(VolunteerOrDonorRegistrationForm):
    if Recaptcha.ENABLE:
        recaptcha = RecaptchaField()
    submit = SubmitField(_l("Next"))


class TeacherForm(StudentOrTeacherRegistrationForm):
    id_card_photo = FileField(_l("Staff Card"), validators=CommonForm.STAFF_CARD_IMAGE_VALIDATORS)
    if Recaptcha.ENABLE:
        recaptcha = RecaptchaField()
    submit = SubmitField(_l("Next"))


class TeacherSecondPageForm(CommonForm):
    school_id = HiddenField(validators=[CommonForm.SchoolId()])
    email = EmailField(_l("Email"),
                       validators=CommonForm.NEW_SCHOOL_EMAIL_VALIDATORS)
    office_phone_number = StringField(
        _l("Office Phone Number"),
        validators=CommonForm.OFFICE_PHONE_VALIDATORS)

    if Recaptcha.ENABLE:
        recaptcha = RecaptchaField()

    submit = SubmitField(_l("Submit"))


class StudentForm(StudentOrTeacherRegistrationForm):
    id_card_photo = FileField(_l("Student Card"), validators=CommonForm.STUDENT_IMAGE_VALIDATORS)
    if Recaptcha.ENABLE:
        recaptcha = RecaptchaField()
    submit = SubmitField(_l("Next"))


class DonorForm(VolunteerOrDonorRegistrationForm):
    if Recaptcha.ENABLE:
        recaptcha = RecaptchaField()
    submit = SubmitField(_l("Register"))


class ResetPasswordRequestForm(CommonForm):
    email = EmailField(_l("Email"), validators=CommonForm.EMAIL_VALIDATORS)
    if Recaptcha.ENABLE:
        recaptcha = RecaptchaField()
    submit = SubmitField(_l("Request Password Reset"))


class ResetPasswordForm(CommonForm):
    password = PasswordField(_l("Password"),
                             validators=CommonForm.PASSWORD_VALIDATORS)
    password2 = PasswordField(_l("Repeat Password"),
                              validators=CommonForm.CONFIRM_PASSWORD_VALIDATORS)
    if Recaptcha.ENABLE:
        recaptcha = RecaptchaField()
    submit = SubmitField(_l("Request Password Reset"))


class StudentSecondPageForm(CommonForm):
    id_card_number = StringField(_l("Hong Kong Identity Card Number"),
                                 validators=CommonForm.IDCARD_VALIDATORS)
    home_address = StringField(_l("Home Address"),
                               validators=CommonForm.ADDRESS_VALIDATORS)
    email = EmailField(_l("Your School Email"), validators=CommonForm.NEW_SCHOOL_EMAIL_VALIDATORS)
    teacher_email = EmailField(_l("Your Teacher email"), validators=CommonForm.EMAIL_VALIDATORS)
    school_id = HiddenField(validators=[CommonForm.SchoolId()])
    latitude = HiddenField(validators=CommonForm.LATITUDE_VALIDATORS)
    longitude = HiddenField(validators=CommonForm.LONGITUDE_VALIDATORS)
    if Recaptcha.ENABLE:
        recaptcha = RecaptchaField()

    submit = SubmitField(_l("Submit"))


class VolunteerSecondPageForm(CommonForm):
    latitude = HiddenField(validators=CommonForm.LATITUDE_VALIDATORS)
    longitude = HiddenField(validators=CommonForm.LONGITUDE_VALIDATORS)
    if Recaptcha.ENABLE:
        recaptcha = RecaptchaField()
    submit = SubmitField(_l("Submit"))
