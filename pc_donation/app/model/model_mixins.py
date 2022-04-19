from datetime import datetime

from flask import current_app
from sqlalchemy import Column, DateTime, FLOAT, String, Index, Float
from sqlalchemy.ext.hybrid import hybrid_property

from app import get_img_url_with_blob_sas_token
from app.azure_ai.face import index_face, PersonGroupEnum
from app.azure_ai.text_analytics import get_thankful_point
from app.common.azure_blob import upload_image_from_memory
from app.length_constants import LengthConstant


class MeetUpMixIn(object):
    time = Column(DateTime, nullable=True)
    latitude = Column(FLOAT(precision=32, decimal_return_scale=None))
    longitude = Column(FLOAT(precision=32, decimal_return_scale=None))
    address = Column(String(220))
    Index("idx_location", latitude, longitude)


class UserPhotoMixIn(object):
    _user_photo = Column(String(LengthConstant.BLOG_LENGTH))
    user_face_index = Column(String(LengthConstant.FACE_INDEX_LENGTH))
    user_type_face_index = Column(String(LengthConstant.FACE_INDEX_LENGTH))

    @hybrid_property
    def user_photo(self):
        return get_img_url_with_blob_sas_token(self._user_photo)

    @user_photo.setter
    def user_photo(self, user_photo_data):
        current_app.logger.info(self.__dict__)
        # TODO: need discuss the file path
        blob_name = self.user_type + "/user/" + self.username + "/" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + "/" + user_photo_data.filename
        upload_image_from_memory(blob_name, user_photo_data)
        user_photo_data.seek(0)  # To enable read again!
        self._user_photo = blob_name
        key = self.user_type + "@" + self.username
        print(type(key))
        self.user_face_index = index_face(PersonGroupEnum.all, key, user_photo_data)
        self.user_type_face_index = index_face(PersonGroupEnum[self.user_type], key, user_photo_data)


class IdCardPhotoMixIn(object):
    _id_card_photo = Column(String(LengthConstant.BLOG_LENGTH))
    id_card_face_index = Column(String(LengthConstant.FACE_INDEX_LENGTH))

    @hybrid_property
    def id_card_photo(self):
        if self._id_card_photo is None:
            return ""
        return get_img_url_with_blob_sas_token(self._id_card_photo)

    @id_card_photo.setter
    def id_card_photo(self, user_photo_data):
        if user_photo_data is None:
            return
        blob_name = self.user_type + "/user/" + self.username + "/" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + "/id_card/" + user_photo_data.filename
        upload_image_from_memory(blob_name, user_photo_data)
        user_photo_data.seek(0)  # To enable read again!
        self._id_card_photo = blob_name


class ThanksPhotoMixIn(object):
    _thanks_photo = Column(String(LengthConstant.BLOG_LENGTH), nullable=True)
    _thanks_message = Column(String(LengthConstant.THANKS_MESSAGE_LENGTH), nullable=True)
    thankfulness = Column(Float, nullable=True)
    happiness = Column(Float, nullable=True)

    @hybrid_property
    def thanks_message(self):
        return self._thanks_message

    @thanks_message.setter
    def thanks_message(self, message):
        self.thankfulness = get_thankful_point(message)
        self._thanks_message = message

    @hybrid_property
    def thanks_photo(self):
        return get_img_url_with_blob_sas_token(self._thanks_photo)

    @thanks_photo.setter
    def thanks_photo(self, photo_data):
        blob_name = self.__class__.__name__ + "/" + self.student.username + "/" + datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S") + "/" + photo_data.filename
        upload_image_from_memory(blob_name, photo_data)
        photo_data.seek(0)  # To enable read again!
        self._thanks_photo = blob_name


class EquipmentPhotoMixIn(object):
    _equipment_photo = Column(String(LengthConstant.BLOG_LENGTH), nullable=True)

    @hybrid_property
    def equipment_photo(self):
        return get_img_url_with_blob_sas_token(self._equipment_photo)

    @equipment_photo.setter
    def equipment_photo(self, photo_data):
        from app.model.models import Equipment, RepairApplication
        current_app.logger.info(self.__dict__)
        if isinstance(self, Equipment):
            blob_name = "/Equipment/" + self.donor.username + "/" + datetime.now().strftime(
                "%Y_%m_%d_%H_%M_%S") + "/" + photo_data.filename
        elif isinstance(self, RepairApplication):
            blob_name = "/RepairApplication/" + self.student.username + "/" + datetime.now().strftime(
                "%Y_%m_%d_%H_%M_%S") + "/" + photo_data.filename
        else:
            raise Exception("EquipmentPhotoMixIn invalid state!")
        upload_image_from_memory(blob_name, photo_data)
        photo_data.seek(0)  # To enable read again!
        self._equipment_photo = blob_name
