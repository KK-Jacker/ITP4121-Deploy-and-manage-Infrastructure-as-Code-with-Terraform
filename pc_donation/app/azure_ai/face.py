import enum
import os
# from PIL import Image, ImageDraw
from functools import cache
from typing import List

from azure.cognitiveservices.vision.face import FaceClient
from flask import current_app
from msrest.authentication import CognitiveServicesCredentials

from config import AiFaceConfig

face_client = FaceClient(AiFaceConfig.ENDPOINT,
                         CognitiveServicesCredentials(AiFaceConfig.KEY))


class PersonGroupEnum(enum.Enum):
    all = 0
    student = 1
    teacher = 2
    donor = 3
    volunteer = 4


@cache
def get_person_group_id(people_group: PersonGroupEnum):
    current_app.logger.info(people_group)
    current_app.logger.info(list(map(lambda g: g.name, face_client.person_group.list())))
    return next(filter(lambda g: g.name == people_group.name, face_client.person_group.list())).person_group_id


def index_face(people_group: PersonGroupEnum, person_id: str, data):
    current_app.logger.info(get_person_group_id(people_group), person_id)
    person_group_person = face_client.person_group_person.create(get_person_group_id(people_group), person_id)
    current_app.logger.info(person_group_person)
    face_client.person_group_person.add_face_from_stream(get_person_group_id(people_group),
                                                         person_group_person.person_id, data)
    data.seek(0)
    return person_group_person.person_id


def is_face_present(people_group: PersonGroupEnum, image, person_ids: List[str]):
    # Detect faces
    face_ids = []
    # We use detection model 3 to get better performance.
    faces = face_client.face.detect_with_url(image, detection_model='detection_03')
    for face in faces:
        face_ids.append(face.face_id)
    # Identify faces
    results = face_client.face.identify(face_ids, get_person_group_id(people_group))

    if not results:
        current_app.logger.info(
            'No person identified in the person group for faces from {}.'.format(os.path.basename(image.name)))
    for person in results:
        if len(person.candidates) > 0:
            current_app.logger.info(
                'Person for face ID {} is identified in {} with a confidence of {}.'.format(person.face_id,
                                                                                            person_ids,
                                                                                            person.candidates[
                                                                                                0].confidence))  # Get topmost confidence score
            current_app.logger.info(person.candidates[0])
            detected_usernames = set(map(lambda x: x.person_id, person.candidates))
            return detected_usernames.issuperset(set(person_ids))
        else:
            return False


def is_face_similar(face1_url: str, face2_url: str):
    # Create an authenticated FaceClient.

    # Detect face(s) from source image 1, returns a list[DetectedFaces]
    # We use detection model 3 to get better performance.
    detected_faces1 = face_client.face.detect_with_url(face1_url,
                                                       detection_model='detection_03')
    # Add the returned face's face ID
    source_image1_id = detected_faces1[0].face_id
    number_of_face1 = len(detected_faces1)

    # Detect face(s) from source image 2, returns a list[DetectedFaces]
    detected_faces2 = face_client.face.detect_with_url(face2_url,
                                                       detection_model='detection_03')

    source_image2_id = detected_faces2[0].face_id
    number_of_face2 = len(detected_faces2)

    if number_of_face1 != 1 or number_of_face2 != 1:
        return False, 1

    verify_result_diff = face_client.face.verify_face_to_face(source_image2_id, source_image1_id)
    current_app.logger.info("Face:" + str(verify_result_diff.confidence))
    return verify_result_diff.is_identical


if __name__ == '__main__':
    # Base url for the Verify and Facelist/Large Facelist operations
    IMAGE_BASE_URL = 'https://csdx.blob.core.windows.net/resources/Face/Images/'
    # Create a list to hold the target photos of the same person
    target_image_file_names = ['Family1-Dad1.jpg', 'Family1-Dad2.jpg']
    # The source photos contain this person
    source_image_file_name1 = 'Family1-Dad3.jpg'
    source_image_file_name2 = 'Family1-Son1.jpg'
    result = is_face_similar(IMAGE_BASE_URL + source_image_file_name1, IMAGE_BASE_URL + source_image_file_name2)
    current_app.logger.info(result)
