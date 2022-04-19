import enum
import re
import typing
from datetime import datetime
from time import time

import jwt
import sqlalchemy
from flask import current_app, session
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, Integer, Column, String, ForeignKey, Boolean, DateTime, Text, Float, FLOAT, Index, Enum, \
    BigInteger, inspect
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy.util import timezone
from werkzeug.security import generate_password_hash, check_password_hash

from app.azure_ai.formrecognizer import extract_receipt
from app.azure_ai.text_analytics import get_urgency_point
from app.azure_ai.translate import translate_to
from app.common.azure_blob import upload_image_from_memory, \
    get_img_url_with_blob_sas_token
from app.length_constants import LengthConstant
from app.model.model_mixins import MeetUpMixIn, UserPhotoMixIn, IdCardPhotoMixIn, ThanksPhotoMixIn, EquipmentPhotoMixIn
from app.model.status_enum import StudentStatusEnum, TeacherStatusEnum, EquipmentStatusEnum, \
    EquipmentApplicationStatusEnum, \
    RepairApplicationStatusEnum, SchoolCategoryEnum, GenderEnum

db = SQLAlchemy(use_native_unicode='utf8')


class UserTypeEnum(enum.Enum):
    admin = 0
    student = 1
    teacher = 2
    donor = 3
    volunteer = 4


class ModelBase(AbstractConcreteBase, db.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @declared_attr
    def __tablename__(cls):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True, onupdate=datetime.now(timezone.utc))

    @classmethod
    def repr(cls, *keys):
        keys = [str(k) for k in keys]
        return '<%s %s>' % (cls.__name__, ', '.join(keys))

    def __repr__(self) -> str:
        if __debug__:
            return "<{}({})>".format(
                self.__class__.__name__,
                ', '.join(
                    ["{}={}".format(k, repr(self.__dict__[k]))
                     for k in sorted(self.__dict__.keys())
                     if k[0] != '_']
                )
            )
        else:
            return self._repr(id=self.id)

    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        """
        Helper for __repr__
        """
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            from sqlalchemy.orm.exc import DetachedInstanceError
            try:
                field_strings.append(f'{key}={field!r}')
            except DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

    def __json__(self):
        return self.fields()

    def fields(self):
        fields = dict()
        for column in self.__table__.columns:
            fields[column.name] = getattr(self, column.name)
        return fields

    def keys(self):
        columns = self.__table__.primary_key.columns
        return tuple([getattr(self, c.name) for c in columns])

    def update(self, fields):
        for column in self.__table__.columns:
            if column.name in fields:
                setattr(self, column.name, fields[column.name])

    def object_as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class User(ModelBase, UserMixin):
    class Meta:
        abstract = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    user_type = Column('user_type', String(10))
    __mapper_args__ = {
        'polymorphic_on': user_type,
        'polymorphic_identity': 'user',
        'with_polymorphic': '*'
    }

    id = Column(Integer, primary_key=True)
    username = Column(String(LengthConstant.USERNAME_LENGTH), index=True, unique=True, nullable=False)
    first_name = Column(String(LengthConstant.NAME_LENGTH), index=True, nullable=False)
    last_name = Column(String(LengthConstant.NAME_LENGTH), index=True, nullable=False)
    first_name_zh_hant = Column(String(LengthConstant.NAME_LENGTH, collation='utf8_bin'), index=True, nullable=False)
    last_name_zh_hant = Column(String(LengthConstant.NAME_LENGTH, collation='utf8_bin'), index=True, nullable=False)

    _email = Column(String(LengthConstant.EMAIL_LENGTH), index=True, unique=True, nullable=False)

    gender = Column(Enum(GenderEnum))
    dateOfBirth = Column(sqlalchemy.Date, nullable=False)

    # 1 Region with 0...* User
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    region = relationship("Region", back_populates="users", foreign_keys=[region_id])

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value.lower().strip()

    phone_number = Column(String(LengthConstant.PHONE_LENGTH), index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    activated = Column(Boolean, default=False)

    last_seen = Column(DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {
                'reset_password': self.id,
                'exp': time() + expires_in
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        jwt_id = jwt.decode(token,
                            current_app.config["SECRET_KEY"],
                            algorithms=["HS256"])["reset_password"]
        return session.get(User, jwt_id)


class Student(UserPhotoMixIn, IdCardPhotoMixIn, User):
    __mapper_args__ = {
        "polymorphic_identity": UserTypeEnum.student.name
    }
    id = Column(Integer, ForeignKey("user.id"), primary_key=True)

    home_address = Column(String(LengthConstant.ADDRESS_LENGTH), nullable=False)
    id_card_number = Column(String(LengthConstant.ID_CARD_LENGTH), nullable=False)

    teacher_email = Column(String(LengthConstant.EMAIL_LENGTH))

    # 1 Student with 0...* EquipmentApplication
    equipment_applications = relationship("EquipmentApplication",
                                          uselist=True,
                                          back_populates="student")

    # 1 Student with 0...* RepairApplication
    repair_applications = relationship("RepairApplication",
                                       uselist=True,
                                       back_populates="student")

    latitude = Column(FLOAT(precision=32, decimal_return_scale=None), nullable=False)
    longitude = Column(FLOAT(precision=32, decimal_return_scale=None), nullable=False)
    Index("idx_location", latitude, longitude)

    # 1 Teacher with 0...* Student
    teacher_id = Column(Integer, ForeignKey("teacher.id"), nullable=True)
    teacher = relationship("Teacher", uselist=False, back_populates="students", foreign_keys=[teacher_id])

    _status = Column(Enum(StudentStatusEnum))

    @hybrid_property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status == StudentStatusEnum.activated:
            self.activated = True
        else:
            self.activated = False
        self._status = status

    # 1 School with many Students
    school_id = Column(BigInteger, ForeignKey("school.id"), nullable=False)
    school = relationship("School", uselist=False, back_populates="students", foreign_keys=[school_id])

    # i student with 0...1 Story
    story = relationship("Story", uselist=False, back_populates="student")


class Teacher(UserPhotoMixIn, IdCardPhotoMixIn, User):
    __mapper_args__ = {
        "polymorphic_identity": UserTypeEnum.teacher.name
    }
    id = Column(Integer, ForeignKey("user.id"), primary_key=True)

    # 1 School with many Teachers
    school_id = Column(BigInteger, ForeignKey("school.id"), nullable=False)
    school = relationship("School", uselist=False, back_populates="teachers", foreign_keys=[school_id])
    office_phone_number = Column(String(LengthConstant.PHONE_LENGTH), index=True, nullable=True)
    _status = Column(Enum(TeacherStatusEnum))

    # 1 Admin with 0...* teacher
    admin_id = Column(Integer, ForeignKey("admin.id"), nullable=True)
    admin = relationship("Admin", uselist=False, back_populates="teachers", foreign_keys=[admin_id])

    # 1 Teacher with 0...* Student
    students = relationship("Student", uselist=True, back_populates="teacher", foreign_keys=[Student.teacher_id])

    @hybrid_property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status == TeacherStatusEnum.activated:
            self.activated = True
        else:
            self.activated = False
        self._status = status


class Donor(UserPhotoMixIn, User):
    __mapper_args__ = {
        "polymorphic_identity": UserTypeEnum.donor.name
    }
    id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    # 1 Donor with 0...* EquipmentApplication
    equipment_applications = relationship("EquipmentApplication",
                                          uselist=True,
                                          back_populates="donor")

    # 1 Donor with 0...* Equipment
    equipments = relationship("Equipment", uselist=True, back_populates="donor")


class Volunteer(UserPhotoMixIn, User):
    __mapper_args__ = {
        "polymorphic_identity": UserTypeEnum.volunteer.name
    }
    id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    latitude = Column(FLOAT(precision=32, decimal_return_scale=None), nullable=False)
    longitude = Column(FLOAT(precision=32, decimal_return_scale=None), nullable=False)
    Index("idx_volunteer_location", latitude, longitude)

    # 1 Volunteer with 0...* RepairApplication
    repair_applications = relationship("RepairApplication",
                                       uselist=True,
                                       back_populates="volunteer")


class EquipmentType(ModelBase):
    id = Column(Integer, primary_key=True)
    name = Column(String(LengthConstant.NAME_LENGTH), unique=True, index=True, nullable=False)

    # 1 EquipmentType with 0...* Equipment
    equipments = relationship("Equipment", uselist=True, back_populates="equipment_type")

    # 1 EquipmentType with 0...* EquipmentApplication
    equipment_applications = relationship("EquipmentApplication", uselist=True, back_populates="equipment_type")


class Equipment(EquipmentPhotoMixIn, ModelBase):
    id = Column(Integer, primary_key=True)
    description = Column(String(LengthConstant.DESCRIPTION_LENGTH, collation='utf8_bin'), nullable=True)
    # For batch import and cross system reference.
    meta = Column(String(LengthConstant.META_LENGTH), nullable=True)
    batch_id = Column(String(LengthConstant.BATCH_LENGTH), nullable=True)

    # 1 EquipmentApplication with 0...1 Equipment
    equipment_application = relationship("EquipmentApplication", back_populates="equipment",
                                         uselist=False)

    # 1 Donor with 0...* Equipment
    donor_id = Column(Integer, ForeignKey("donor.id"), nullable=False)
    donor = relationship("Donor", back_populates="equipments", foreign_keys=[donor_id])

    # 1 EquipmentType with 0...* Equipment
    equipment_type_id = Column(Integer, ForeignKey("equipment_type.id"), nullable=False)
    equipment_type = relationship("EquipmentType", back_populates="equipments", foreign_keys=[equipment_type_id])

    status = Column(Enum(EquipmentStatusEnum))

    has_receipt = Column(Boolean, default=False)
    _receipt_photo = Column(String(LengthConstant.BLOG_LENGTH), nullable=True)
    receipt_total = Column(Float, nullable=True)
    receipt_date = Column(DateTime, nullable=True)
    receipt_merchant_name = Column(String(LengthConstant.TITLE_LENGTH), nullable=True)
    receipt_reject_reason = Column(String(LengthConstant.MESSAGE_LENGTH), nullable=True)

    # 1 Admin with 0...* Equipment
    admin_id = Column(Integer, ForeignKey("admin.id"), nullable=True)
    admin = relationship("Admin", uselist=False, back_populates="equipments", foreign_keys=[admin_id])

    @hybrid_property
    def receipt_photo(self):
        return get_img_url_with_blob_sas_token(self._receipt_photo)

    @receipt_photo.setter
    def receipt_photo(self, photo_data):
        if photo_data is None:
            return
        blob_name = "/receipt/" + self.donor.username + "/" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + "/" + photo_data.filename
        upload_image_from_memory(blob_name, photo_data)
        photo_data.seek(0)  # To enable read again!
        self._receipt_photo = blob_name
        receipt_url = get_img_url_with_blob_sas_token(self._receipt_photo)
        receipt = extract_receipt(receipt_url)
        self.receipt_total = receipt.total
        self.receipt_date = receipt.date
        self.receipt_merchant_name = receipt.merchant_name
        self.has_receipt = True


class Admin(User):
    __mapper_args__ = {
        "polymorphic_identity": UserTypeEnum.admin.name
    }
    id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    # 1 Admin with 0...* Teacher
    teachers = relationship("Teacher", uselist=True, back_populates="admin", foreign_keys=[Teacher.admin_id])
    # 1 Admin with 0...* Equipment
    equipments = relationship("Equipment", uselist=True, back_populates="admin", foreign_keys=[Equipment.admin_id])


class EquipmentApplication(MeetUpMixIn, ThanksPhotoMixIn, ModelBase):
    id = Column(Integer, primary_key=True)
    status = Column(Enum(EquipmentApplicationStatusEnum))

    # 1 EquipmentType with 0...* EquipmentApplication
    equipment_type_id = Column(Integer, ForeignKey("equipment_type.id"), nullable=False)
    equipment_type = relationship("EquipmentType", uselist=False, back_populates="equipment_applications",
                                  foreign_keys=[equipment_type_id])

    # 1 Student with 0...* EquipmentApplication
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    student = relationship("Student", uselist=False, back_populates="equipment_applications", foreign_keys=[student_id])

    # 1 Donor with 0...* EquipmentApplication
    donor_id = Column(Integer, ForeignKey("donor.id"), nullable=True)
    donor = relationship("Donor", uselist=False, back_populates="equipment_applications", foreign_keys=[donor_id])

    # 1 EquipmentApplication with 0...1 Equipment
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=True)
    equipment = relationship("Equipment",
                             back_populates="equipment_application",
                             uselist=False,
                             foreign_keys=[equipment_id])

    # 1 EquipmentApplication with 0...1 Message
    messages = relationship("Message",
                            back_populates="equipment_application",
                            lazy="dynamic",
                            uselist=True)


# Student ask for Support
class RepairApplication(MeetUpMixIn, ThanksPhotoMixIn, EquipmentPhotoMixIn, ModelBase):
    id = Column(Integer, primary_key=True)
    title = Column(String(LengthConstant.TITLE_LENGTH), nullable=False)
    description = Column(String(LengthConstant.DESCRIPTION_LENGTH, collation='utf8_bin'), nullable=False)
    status = Column(Enum(RepairApplicationStatusEnum), nullable=False)

    # 1 Student with 0...* RepairApplication
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    student = relationship("Student", uselist=False, back_populates="repair_applications", foreign_keys=[student_id])

    # 1 Volunteer with 0...* RepairApplication
    volunteer_id = Column(Integer, ForeignKey("volunteer.id"), nullable=True)
    volunteer = relationship("Volunteer", uselist=False, back_populates="repair_applications",
                             foreign_keys=[volunteer_id])

    # 1 RepairApplication with 0...1 Message
    messages = relationship("Message",
                            back_populates="repair_application",
                            lazy="dynamic",
                            uselist=True)


class Message(ModelBase):
    id = Column(Integer, primary_key=True)
    message = Column(String(LengthConstant.MESSAGE_LENGTH), nullable=False)

    from_student = Column(Boolean, nullable=False)

    # 1 EquipmentApplication with 0...1 Message
    equipment_application_id = Column(Integer, ForeignKey('equipment_application.id'), nullable=True)
    equipment_application = relationship('EquipmentApplication',
                                         back_populates='messages',
                                         foreign_keys=[equipment_application_id])

    # 1 EquipmentApplication with 0...1 Message
    repair_application_id = Column(Integer, ForeignKey("repair_application.id"), nullable=True)
    repair_application = relationship("RepairApplication",
                                      back_populates="messages",
                                      foreign_keys=[repair_application_id])


class School(ModelBase):
    id = Column(BigInteger, primary_key=True)
    name_en = Column(String(200, collation='utf8_bin'), nullable=False)
    name_zh_Hant = Column(String(100, collation='utf8_bin'), nullable=False)
    address_en = Column(String(500, collation='utf8_bin'), nullable=False)
    address_zh_Hant = Column(String(150, collation='utf8_bin'), nullable=False)
    url = Column(String(200), nullable=False)
    phone_number = Column(String(20), nullable=False)
    latitude = Column(FLOAT(precision=32, decimal_return_scale=None), nullable=False)
    longitude = Column(FLOAT(precision=32, decimal_return_scale=None), nullable=False)

    category = Column(Enum(SchoolCategoryEnum), nullable=False)
    # 1 School with many Students
    students = relationship("Student", back_populates="school", uselist=True)
    # 1 School with many Teachers
    teachers = relationship("Teacher", back_populates="school", uselist=True)
    # # 1 Region with 0...* Student
    region_id = Column(Integer, ForeignKey("region.id"))
    region = relationship("Region", back_populates="schools", foreign_keys=[region_id])


class Region(ModelBase):
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, index=True, nullable=False)

    # 1 Region with 0...* Student
    # students = relationship('Student', uselist=True, back_populates='region', foreign_keys=[Student.region_id])
    # 1 Region with 0...* User
    users = relationship("User", uselist=True, back_populates="region", foreign_keys=[User.region_id])
    # 1 Region with 0...* School
    schools = relationship("School", uselist=True, back_populates="region", foreign_keys=[School.region_id])


class Story(ModelBase):
    id = Column(Integer, primary_key=True)
    title = Column(String(LengthConstant.TITLE_LENGTH, collation='utf8_bin'))
    title_zh_Hant = Column(String(LengthConstant.TITLE_LENGTH, collation='utf8_bin'))
    title_en = Column(String(LengthConstant.TITLE_LENGTH))
    content = Column(Text(collation='utf8_bin'))
    content_zh_Hant = Column(Text(collation='utf8_bin'))
    content_en = Column(Text(collation='utf8_bin'))
    urgency = Column(Float, index=True)
    _story_photo = Column(String(LengthConstant.BLOG_LENGTH), nullable=True)

    @hybrid_property
    def story_photo(self):
        return get_img_url_with_blob_sas_token(self._story_photo)

    @story_photo.setter
    def story_photo(self, photo_data):
        blob_name = "student/" + self.student.username + "/" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + "/" + photo_data.filename
        upload_image_from_memory(blob_name, photo_data)
        photo_data.seek(0)  # To enable read again!
        self._story_photo = blob_name

    approved = Column(Boolean, default=False)
    # i student with 0...1 Story
    student_id = Column(Integer, ForeignKey("student.id"))
    student = relationship("Student", back_populates="story")


@event.listens_for(Story, "before_insert")
def translate_story_before_insert(mapper, connect, target):
    translate_story(target)


@event.listens_for(Story, "before_update")
def translate_story_before_update(mapper, connection, target):
    translate_story(target)


def translate_story(target):
    sources = [target.title, target.content]
    # TODO: Hant Capital Problem
    translated_texts_zh_hant = translate_to(sources, "zh-Hant").translated_texts
    translated_texts_en = translate_to(sources, "en").translated_texts
    target.title_zh_Hant = translated_texts_zh_hant[0]
    target.title_en = translated_texts_en[0]
    target.content_zh_Hant = translated_texts_zh_hant[1]
    target.content_en = translated_texts_en[1]
    target.urgency = get_urgency_point(target.content)
