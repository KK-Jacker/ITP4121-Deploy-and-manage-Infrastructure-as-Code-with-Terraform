import re
from datetime import datetime, timedelta

from flask import current_app
from flask_babel import _, lazy_gettext as _l
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileAllowed, FileRequired
from sqlalchemy.orm import with_polymorphic
from tldextract import tldextract
from wtforms import ValidationError, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, URL, InputRequired, NumberRange

from app.azure_ai.face import is_face_similar
from app.azure_ai.text_analytics import is_content_ok
from app.azure_ai.vision import vision_analyze
from app.common.azure_blob import upload_image_from_memory, get_img_url_with_blob_sas_token
from app.length_constants import LengthConstant
from app.model.models import User, Teacher, School


class CommonForm(FlaskForm):
    class NewUsername(object):
        def __call__(self, form, field):
            username = field.data

            if re.search("[-+!@#$%^&*(){}<>_=~`:;?/,.|]",
                         username) is not None:
                raise ValidationError(
                    _("Please make sure your full name does not contain special character in it"
                      ))
            all_users = with_polymorphic(User, "*")
            user = all_users.query.filter_by(username=username).first()
            if user is not None:
                raise ValidationError(_("Please use a different username."))

    class Password(object):
        def __call__(self, form, field):
            password = field.data
            if re.search("[0-9]", password) is None:
                raise ValidationError(
                    _("Please make sure your password at least one number in it"
                      ))
            elif re.search("[A-Z]", password) is None:
                raise ValidationError(
                    _("Please make sure your password at least one capital letter in it"
                      ))
            elif re.search("[a-z]", password) is None:
                raise ValidationError(
                    _("Please make sure your password at least one lowercase letter in it"
                      ))
            elif re.search("[-+!@#$%^&*(){}><_=~`:;?/,.|]", password) is None:
                raise ValidationError(
                    _("Please make sure your password at least one special character in it"
                      ))

    class Name(object):
        def __call__(self, form, field):
            full_name = field.data
            if re.search("[-+!@#$%^&*(){}<>_=~`:;?/,.| ]",
                         full_name) is not None:
                raise ValidationError(_("No special character or space"))

    class Birth(object):
        def __call__(self, form, field):
            birth = field.data
            if re.match("^\d{4}-\d{2}-\d{2}$",
                         birth) is None:
                raise ValidationError(_("Wrong Date Format"))

    class Address(object):
        def __call__(self, form, field):
            address = field.data
            if re.search("[+!@#$%^&*(){}<>_=~`:;?/|]",
                         address) is not None:
                raise ValidationError(_("No special character or space"))

    class IDCard(object):
        def __call__(self, form, field):
            birth = field.data
            if re.match("^[a-zA-Z]{1}\d{7}$",
                         birth) is None:
                raise ValidationError(_("Wrong ID Card Format"))

    class Gender(object):
        def __call__(self, form, field):
            birth = field.data
            if re.match("^[M|F]$",
                         birth) is None:
                raise ValidationError(_("Wrong Gender Format"))

    class UsernameOrEmail(object):
        def __call__(self, form, field):
            login = field.data
            if re.search("[-+!#$%^&*(){}<>_=~`:;?/,| ]",
                         login) is not None:
                raise ValidationError(_("No special character or space"))

    class PhoneNumber(object):
        def __call__(self, form, field):
            phone_number = field.data
            if re.search("[0-9]", phone_number) is None:
                raise ValidationError(_("Please use digits."))

    class DuplicateEmail(object):
        def __call__(self, form, field):
            email = field.data
            all_users = with_polymorphic(User, "*")
            user = all_users.query.filter_by(email=email.lower()).first()
            if user is not None:
                raise ValidationError(
                    _("Please use a different email address."))

    class SchoolEmail(object):
        def __call__(self, form, field):
            email = field.data
            if not email.lower().endswith("edu.hk"):
                raise ValidationError(_("The email must be school email"))

    class SchoolName(object):
        def __call__(self, form, field):
            name = field.data
            if re.search("[-+!@#$%^&*(){}><_=~`:;?/,.|]", name) is not None:
                raise ValidationError(
                    _("Please make sure your school name does not contain special character in it"
                      ))
            elif re.search("[0-9]", name) is not None:
                raise ValidationError(
                    _("Please make sure your school name does not contain digit in it"
                      ))

    class OfficePhoneNumber(object):
        def __call__(self, form, field):
            office_phone_number = field.data
            user = Teacher.query.filter_by(
                office_phone_number=office_phone_number).first()
            if user is not None:
                raise ValidationError(
                    _("Please use a different office phone number."))

    class ContainString(object):
        def __init__(self, check, message=None):
            self.message = message
            self.check = check

        def __call__(self, form, field):
            value = field.data
            if self.check not in value:
                if self.message is not None:
                    raise ValidationError(self.message)
                raise ValidationError(
                    _("Must contain " + self.check))

    class ModerateImage(object):
        def __init__(self, check_age_range=False, check_face=True):
            self.check_face = check_face
            self.check_age_range = check_age_range

        def __call__(self, form, field):
            if field.data is None:
                return
            blob_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + field.data.filename
            upload_image_from_memory(blob_name, field.data, temp=True)
            field.data.seek(0)  # To enable read again!
            url = get_img_url_with_blob_sas_token(blob_name, temp=True)
            image_error = vision_analyze(url, check_age_range=self.check_age_range, check_face=self.check_face)
            if image_error is not None:
                raise ValidationError(image_error)

    class FileSize(object):
        def __init__(self, minimum=0.2, maximum=5120):
            self.minimum = minimum
            self.maximum = maximum

        def __call__(self, form, field):
            if field.data is None:
                return
            blob = field.data.read()
            size = len(blob) / 1024  # to kb
            # To enable read again!
            field.data.seek(0)
            if size < self.minimum:
                raise ValidationError(_("File size should be bigger than ") + str(self.minimum) + " kb")
            if size > self.maximum:
                raise ValidationError(_("File size should be smaller than ") + str(self.maximum) + " mb")

    class FaceEqualTo(object):
        def __init__(self, fieldname, message=None):
            self.fieldname = fieldname
            self.message = message

        def __call__(self, form, field):
            other = form[self.fieldname]
            if field.data is None or other.data is None:
                return
            blob_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + "face1/" + field.data.filename
            upload_image_from_memory(blob_name, field.data, temp=True)
            field.data.seek(0)  # To enable read again!
            face1_url = get_img_url_with_blob_sas_token(blob_name, temp=True)

            blob_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + "face2/" + other.data.filename
            upload_image_from_memory(blob_name, other.data, temp=True)
            other.data.seek(0)  # To enable read again!
            face2_url = get_img_url_with_blob_sas_token(blob_name, temp=True)
            if not is_face_similar(face1_url, face2_url):
                raise ValidationError(_("Face is not the same!"))

    class ModerateText(object):
        def __init__(self, check_pii=False):
            self.check_pii = check_pii

        def __call__(self, form, field):
            value = field.data
            if value and not is_content_ok(value, self.check_pii):
                if self.check_pii:
                    raise ValidationError(
                        _("Found offensive content, sexually explicit or suggestive content, profanity, and personal "
                          "data."))
                else:
                    raise ValidationError(
                        _("Found offensive content, sexually explicit or suggestive content, and profanity"))

    class FutureDateTime(object):
        def __init__(self, day=3, message=None):
            self.message = message
            self.day = day

        def __call__(self, form, field):
            value = field.data
            delta = value - datetime.now()
            current_app.logger.info(delta.days)
            if delta.days < self.day:
                if self.message is not None:
                    raise ValidationError(self.message)
                raise ValidationError(
                    _("At least wait for {x} days").replace("{x}", str(self.day)))

    class SchoolId(object):
        def __call__(self, form, field):
            school_id = field.data
            school = School.query.filter_by(id=school_id).first()
            if school is None:
                raise ValidationError(_("School ID does not exist."))

    class SchoolDomainEmail(object):
        def __init__(self, fieldname="school_id", message=None):
            self.fieldname = fieldname
            self.message = message

        def __call__(self, form, field):
            try:
                school_id = form[self.fieldname].data
            except KeyError:
                raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
            school = School.query.filter_by(id=school_id).first()
            registered_domain = tldextract.extract(school.url).registered_domain
            current_app.logger.info(field.data)
            current_app.logger.info(registered_domain)
            if not field.data.endswith(registered_domain):
                message = self.message
                raise ValidationError(_("Email must be end with " + registered_domain))

    MAX_TEXT_LENGTH = 1000
    EMAIL_VALIDATORS = [
        DataRequired(),
        Email(),
        Length(min=10, max=LengthConstant.EMAIL_LENGTH)
    ]
    # noinspection PyTypeChecker
    NEW_EMAIL_VALIDATORS = EMAIL_VALIDATORS + [DuplicateEmail()]
    NEW_SCHOOL_EMAIL_VALIDATORS = NEW_EMAIL_VALIDATORS + [SchoolEmail(), SchoolDomainEmail()]

    USERNAME_VALIDATORS = [
        DataRequired(),
        Length(min=3, max=LengthConstant.USERNAME_LENGTH),
        Name(),
        ModerateText()
    ]
    LOGIN_VALIDATORS = [
        DataRequired(),
        Length(min=3, max=LengthConstant.EMAIL_LENGTH),
        UsernameOrEmail(),
        ModerateText()
    ]

    ADDRESS_VALIDATORS = [
        DataRequired(),
        Length(min=3, max=LengthConstant.ADDRESS_LENGTH),
        Address(),
        ModerateText()
    ]

    BIRTH_VALIDATORS = [
        DataRequired(),
        Birth(),
        ModerateText()
    ]

    IDCARD_VALIDATORS = [
        DataRequired(),
        IDCard(),
        ModerateText()
    ]

    # noinspection PyTypeChecker
    NEW_USERNAME_VALIDATORS = USERNAME_VALIDATORS + [NewUsername()]

    NAME_VALIDATORS = [DataRequired(), Length(min=LengthConstant.MIN_NAME_LENGTH, max=LengthConstant.NAME_LENGTH), Regexp("[a-zA-Z]")]

    CHI_NAME_VALIDATORS = [
        DataRequired(),
        Length(min=LengthConstant.MIN_CHI_NAME_LENGTH, max=LengthConstant.NAME_LENGTH),
        Name(),
        ModerateText()
    ]

    PASSWORD_VALIDATORS = [
        DataRequired(),
        Regexp(r"^[\w.@+-]+$"),
        Length(min=8, max=LengthConstant.NAME_LENGTH),
        Password(),
        ModerateText()
    ]
    # noinspection PyTypeChecker
    CONFIRM_PASSWORD_VALIDATORS = PASSWORD_VALIDATORS + [
        EqualTo("password", message=_l("pass_error"))
    ]

    PHONE_VALIDATORS = [DataRequired(), Length(min=8, max=LengthConstant.PHONE_LENGTH), PhoneNumber()]

    _BASIC_IMAGE_VALIDATORS = [
        FileAllowed(["jpg", "png", "jpeg"]),
        FileSize()
    ]
    # noinspection PyTypeChecker
    IMAGE_VALIDATORS = _BASIC_IMAGE_VALIDATORS + [FileRequired(), ModerateImage()]
    # noinspection PyTypeChecker
    STUDENT_IMAGE_VALIDATORS = _BASIC_IMAGE_VALIDATORS + [FileRequired(), ModerateImage(check_age_range=True),
                                                          FaceEqualTo("user_photo")]
    # noinspection PyTypeChecker
    NO_FACE_IMAGE_VALIDATORS = _BASIC_IMAGE_VALIDATORS + [FileRequired(),
                                                          ModerateImage(check_age_range=False, check_face=False)]

    # noinspection PyTypeChecker
    RECEIPT_IMAGE_VALIDATORS = _BASIC_IMAGE_VALIDATORS + [ModerateImage(check_age_range=False, check_face=False)]
    # noinspection PyTypeChecker
    STAFF_CARD_IMAGE_VALIDATORS = _BASIC_IMAGE_VALIDATORS + [ModerateImage(check_age_range=False, check_face=False),
                                                             FaceEqualTo("user_photo")]
    OPTIONAL_MESSAGE_VALIDATORS = [
        Length(min=0, max=LengthConstant.MESSAGE_LENGTH),
        ModerateText(check_pii=True)
    ]

    MESSAGE_VALIDATORS = [DataRequired(), Length(min=2, max=LengthConstant.MESSAGE_LENGTH),
                          ModerateText(check_pii=True)]

    THANKS_VALIDATORS = [
        DataRequired(),
        Length(min=10, max=LengthConstant.THANKS_MESSAGE_LENGTH),
        ModerateText(check_pii=True)
    ]

    TITTLE_VALIDATORS = [
        DataRequired(),
        Length(min=5, max=LengthConstant.TITLE_LENGTH),
        ModerateText(check_pii=True)
    ]

    STORY_VALIDATORS = [
        DataRequired(),
        Length(min=50, max=MAX_TEXT_LENGTH),
        ModerateText(check_pii=True)
    ]

    SCHOOL_NAME_VALIDATORS = [
        DataRequired(),
        Length(min=5, max=200),
        SchoolName(),
        ModerateText(check_pii=True)
    ]

    SCHOOL_URL_VALIDATORS = [
        DataRequired(),
        Length(min=5, max=200),
        URL(),
        ContainString(check="edu.hk")
    ]

    DESCRIPTION_VALIDATORS = [
        DataRequired(),
        Length(min=10, max=MAX_TEXT_LENGTH),
        ModerateText()
    ]

    OFFICE_PHONE_VALIDATORS = [
        DataRequired(),
        Length(min=8, max=LengthConstant.PHONE_LENGTH),
        OfficePhoneNumber()
    ]

    MEET_UP_DATE_TIME_VALIDATORS = [DataRequired(), FutureDateTime(), InputRequired()]

    LATITUDE_VALIDATORS = [DataRequired()]
    LONGITUDE_VALIDATORS = [DataRequired()]
    #REGION_VALIDATORS = [DataRequired(), NumberRange(min=0, message=_("Please select region."))]

    SELECT_VALIDATORS = [DataRequired(), NumberRange(min=0, message=_("Please select option."))]


class DateTimeField(StringField):
    def process_formdata(self, datetime_string):
        current_app.logger.info(datetime_string[0])
        data = datetime.strptime(datetime_string[0], "%d/%m/%Y %H:%M %p")
        super().process_formdata([data])

class DateField(StringField):
    def process_formdata(self, datetime_string):
        current_app.logger.info(datetime_string[0])
        data = datetime.strptime(datetime_string[0], "%d/%m/%Y")
        super().process_formdata([data])


class ApprovalForm(CommonForm):
    username = StringField(_l("Username"), validators=CommonForm.USERNAME_VALIDATORS, render_kw={"readonly": True})
    first_name = StringField(_l("First Name"), validators=CommonForm.NAME_VALIDATORS,
                             render_kw={"readonly": True})
    last_name = StringField(_l("Last Name"), validators=CommonForm.NAME_VALIDATORS,
                            render_kw={"readonly": True})
    email = StringField(_l("Email"), validators=CommonForm.EMAIL_VALIDATORS, render_kw={"readonly": True})
    phone_number = StringField(_l("Phone Number"), validators=CommonForm.PHONE_VALIDATORS,
                               render_kw={"readonly": True})
    school_name = StringField(_l("School Name", validators=CommonForm.SCHOOL_NAME_VALIDATORS),
                              render_kw={"readonly": True})
    school_URL = StringField(_l("School Website"), validators=CommonForm.SCHOOL_URL_VALIDATORS,
                             render_kw={"readonly": True})


class MsgForm(CommonForm):
    message = StringField(validators=CommonForm.MESSAGE_VALIDATORS)
    submit = SubmitField(_l("Send Message"))


class RecaptchaMsgForm(MsgForm):
    recaptcha = RecaptchaField()


def get_msg_form(messages):
    d = datetime.now()
    d = d + timedelta(minutes=-1)
    is_too_frequent = len(list(filter(lambda x: x.created_at > d, messages))) > 10
    return RecaptchaMsgForm() if is_too_frequent else MsgForm()
