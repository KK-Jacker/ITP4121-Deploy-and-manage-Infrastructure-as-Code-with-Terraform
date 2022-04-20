import random as rand
from datetime import date
from functools import wraps
from time import time

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

from app import SQLAlchemy, create_app
from app.azure_ai.face import PersonGroupEnum
from app.model.models import Region, EquipmentType, Admin, School, Student, Teacher, Volunteer, \
    Story, RepairApplication, Donor, Equipment, EquipmentApplication
from app.model.status_enum import StudentStatusEnum, TeacherStatusEnum, EquipmentStatusEnum, \
    EquipmentApplicationStatusEnum, \
    RepairApplicationStatusEnum, SchoolCategoryEnum, GenderEnum
# The default password is P@ssw0rd.
from config import AiFaceConfig

password_hash = "pbkdf2:sha256:150000$hIcu3Dhn$5590ce353d7d4cebea1b85be035dcf4d19bc142501d6d1259c9b2de06ed081e8"
photo_blob = "donor/user/donor/2021_07_13_04_11_38/Donor.jpg"

number_of_student = 10
number_of_volunteer = 10
number_of_donor = 5
number_of_school = 10
number_of_equipment = 10
number_of_teacher = 100
number_of_repair_applications_per_student = 100
number_of_equipment_applications_per_student = 50


def timer(func):
    @wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(time() * 1000)) - start
            print(func.__name__ + f" total execution time: {end_ if end_ > 0 else 0} ms")

    return _time_it


def random_story():
    sentences = ["I am poor!", "very unhappy!", "My father is dead!", "My mother is in sick!", "Today is Monday",
                 "This is a cat", "Very bad", "I don't have a computer and I cannot take online class.",
                 "Today is my happy birthday!", "I am good!", "it is very nice!",
                 "我很窮！", "很不開心！", "我爸爸死了！", "我媽媽生病了！", "今天是星期一",
                 "這是一隻貓", "很糟糕", "我沒有電腦,不能上網課。",
                 "今天是我的生日快樂！", "我很好！", "真好！"]
    return ' '.join(rand.sample(sentences, rand.randint(2, rand.randint(2, 6))))


def random_repair_details():
    sentences = ["My PC cannot connect internet!", "My computer cannot boot up!", "My monitor is not working.",
                 "I don't  know how to fix reset my router password."
                 "我的電腦無法連接互聯網！", "我的電腦無法啟動！", "我的顯示器不工作。",
                 "我不知道如何修復重置我的路由器密碼。"
                 ]
    return ' '.join(rand.sample(sentences, rand.randint(2, rand.randint(2, 6))))


def random_latitude():
    return (22.4393278 - 22.1193278) * rand.randint(0, 500) / 1000 + 22.1193278


def random_longitude():
    return (114.3228131 - 114.0028131) * rand.randint(500, 1000) / 1000 + 114.0028131


def get_sample_school():
    return db.session.query(School).limit(number_of_school).all()


app = create_app()
db = SQLAlchemy(app, use_native_unicode='utf8')


@timer
def region_data():
    r = ['CENTRAL AND WESTERN',
         'EASTERN',
         'ISLANDS',
         'KOWLOON CITY',
         'KWAI TSING',
         'KWUN TONG',
         'NORTH',
         'SAI KUNG',
         'SHA TIN',
         'SHAM SHUI PO',
         'SOUTHERN',
         'TAI PO',
         'TSUEN WAN',
         'TUEN MUN',
         'WAN CHAI',
         'WONG TAI SIN',
         'YAU TSIM MONG',
         'YUEN LONG',
         ]
    db.session.add_all(list(map(lambda x: Region(name=x), r)))
    db.session.commit()


@timer
def school_data():
    import csv
    schools = []
    mapping = {
        'Aided Primary Schools': SchoolCategoryEnum.AIDED_PRIMARY_SCHOOLS,
        'Aided Secondary Schools': SchoolCategoryEnum.AIDED_SECONDARY_SCHOOLS,
        'Aided Special Schools': SchoolCategoryEnum.AIDED_SPECIAL_SCHOOLS,
        'Caput Secondary Schools': SchoolCategoryEnum.CAPUT_SECONDARY_SCHOOLS,
        'Direct Subsidy Scheme Primary Schools': SchoolCategoryEnum.DIRECT_SUBSIDY_SCHEME_PRIMARY_SCHOOLS,
        'Direct Subsidy Scheme Secondary Schools': SchoolCategoryEnum.DIRECT_SUBSIDY_SCHEME_SECONDARY_SCHOOLS,
        'English Schools Foundation (Primary)': SchoolCategoryEnum.ENGLISH_SCHOOLS_FOUNDATION_PRIMARY,
        'English Schools Foundation (Secondary)': SchoolCategoryEnum.ENGLISH_SCHOOLS_FOUNDATION_SECONDARY,
        'Government Primary Schools': SchoolCategoryEnum.GOVERNMENT_PRIMARY_SCHOOLS,
        'Government Secondary Schools': SchoolCategoryEnum.GOVERNMENT_SECONDARY_SCHOOLS,
        'International Schools (Primary)': SchoolCategoryEnum.INTERNATIONAL_SCHOOLS_PRIMARY,
        'International Schools (Secondary)': SchoolCategoryEnum.INTERNATIONAL_SCHOOLS_SECONDARY,
        'Kindergarten-cum-child Care Centres': SchoolCategoryEnum.KINDERGARTEN_CUM_CHILD_CARE_CENTRES,
        'Kindergartens': SchoolCategoryEnum.KINDERGARTENS,
        'Private Primary Schools': SchoolCategoryEnum.PRIVATE_PRIMARY_SCHOOLS,
        'Private Secondary Schools (Day/Evening)': SchoolCategoryEnum.PRIVATE_SECONDARY_SCHOOLS_DAY_EVENING,
    }

    with open('data/SCH_LOC_EDB.csv', newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')

        for row in reader:
            school = School()
            school.id = row['\ufeffSCHOOL NO.']
            school.name_en = row['ENGLISH NAME']
            school.name_zh_Hant = row['中文名稱']
            school.address_en = row['ENGLISH ADDRESS']
            school.address_zh_Hant = row['中文地址']
            school.url = row['WEBSITE']
            school.phone_number = row['TELEPHONE']
            school.latitude = row['LATITUDE']
            school.longitude = row['LONGITUDE']
            school.region = db.session.query(Region).filter_by(name=row['DISTRICT']).first()
            school.category = mapping[row['ENGLISH CATEGORY']]
            # print(school)
            schools.append(school)
    db.session.add_all(schools)
    db.session.commit()


@timer
def equipment_type_data():
    r = ['Desktop', 'Laptop', 'Router', 'Mobile phone', 'SIM card', 'Keyboard', 'Mouse', 'Monitor', 'Microphone',
         'Headphone', 'Webcam', 'Tablet', "Window/Office Licence"]

    db.session.add_all(list(map(lambda x: EquipmentType(name=x), r)))

    db.session.commit()


@timer
def admin_data():
    admin = Admin(first_name="Cyrus", last_name="Wong", username="admin", email="vtcfyp123@gmail.com",
                  phone_number=12345678,
                  password_hash=password_hash,
                  gender=GenderEnum.MALE,
                  first_name_zh_hant="Admin",
                  last_name_zh_hant="last_name_zh_hant",
                  dateOfBirth=date.fromisoformat('2019-12-04'),
                  activated=True, region_id=1)
    db.session.add_all([admin])
    db.session.commit()
    print(admin)


@timer
def teacher_data():
    schools = get_sample_school()
    teachers = list(
        map(lambda x: Teacher(first_name="Teacher " + str(x), last_name="Lam", username="teacher" + str(x),
                              email=str(x) + "teacher@vtc.edu.hk",
                              phone_number=90000000 + x,
                              password_hash=password_hash,
                              activated=True, region_id=1,
                              gender=GenderEnum.MALE,
                              first_name_zh_hant="老師 " + str(x),
                              last_name_zh_hant="last_name_zh_hant",
                              dateOfBirth=date.fromisoformat('2019-12-04'),
                              _user_photo="teacherB2021_05_21_11_52_27_teacher_photo_Sam_1",
                              _id_card_photo="teacherB2021_05_21_11_52_27_staff_card_student_picture.png",
                              user_face_index="4ae75b05-22d2-41be-b881-9203534d90b0",
                              status=TeacherStatusEnum.activated,
                              school=schools[rand.randint(0, number_of_school - 1)],
                              admin_id=1,
                              office_phone_number=97346783), range(1, number_of_teacher)))

    teacher_user = Teacher(first_name="Sam", last_name="Lam", username="teacherA",
                           email="190337259@stu.vtc.edu.hk",
                           phone_number=97986524,
                           password_hash=password_hash,
                           activated=True, region_id=1,
                           gender=GenderEnum.MALE,
                           first_name_zh_hant="老師",
                           last_name_zh_hant="last_name_zh_hant",
                           dateOfBirth=date.fromisoformat('2019-12-04'),
                           _user_photo="teacherB2021_05_21_11_52_27_teacher_photo_Sam_1",
                           user_face_index="4ae75b05-22d2-41be-b881-9203534d90b0",
                           _id_card_photo="teacherB2021_05_21_11_52_27_staff_card_student_picture.png",
                           status=TeacherStatusEnum.activated, school=schools[0], admin_id=1,
                           office_phone_number=97346783)
    db.session.add_all([teacher_user] + teachers)
    db.session.commit()
    print(teacher_user)


@timer
def student_data():
    schools = get_sample_school()
    students = list(
        map(lambda x: Student(first_name="First Name " + str(x), last_name="Lam", username="student" + str(x),
                              email=str(x) + "@stu.vtc.edu.hk",
                              phone_number=90000000 + x,
                              password_hash=password_hash,
                              activated=True, region_id=1,
                              gender=GenderEnum.MALE,
                              first_name_zh_hant="學生 " + str(x),
                              last_name_zh_hant="last_name_zh_hant",
                              home_address="home_address",
                              id_card_number="A1234567",
                              dateOfBirth=date.fromisoformat('2019-12-04'),
                              _user_photo=photo_blob,
                              user_face_index="4ae75b05-22d2-41be-b881-9203534d90b0",
                              _id_card_photo=photo_blob,
                              latitude=random_latitude(), longitude=random_longitude(),
                              status=StudentStatusEnum.activated,
                              teacher_id=2, school=schools[rand.randint(0, number_of_school - 1)],
                              story=Story(title="title " + str(x), content=random_story(),
                                          _story_photo=photo_blob,
                                          approved=True),
                              teacher_email="190337259@stu.vtc.edu.hk"), range(1, number_of_student)))

    student_user = Student(first_name="Pak Yin", last_name="Lam", username="studentA",
                           email="190110723@stu.vtc.edu.hk",
                           phone_number=97989954,
                           password_hash=password_hash,
                           activated=True, region_id=1,
                           gender=GenderEnum.MALE,
                           first_name_zh_hant="學生 X",
                           last_name_zh_hant="last_name_zh_hant",
                           home_address="home_address",
                           id_card_number="A1234567",
                           dateOfBirth=date.fromisoformat('2019-12-04'),
                           _user_photo=photo_blob,
                           user_face_index="4ae75b05-22d2-41be-b881-9203534d90b0",
                           _id_card_photo=photo_blob,
                           latitude=22.272776384977455, longitude=114.18772674351163,
                           teacher_id=2, status=StudentStatusEnum.activated, school=schools[0],
                           teacher_email="190337259@stu.vtc.edu.hk", story=Story(title="title ",
                                                                                 content=random_story(),
                                                                                 _story_photo=photo_blob,
                                                                                 approved=True))
    db.session.add_all([student_user] + students)
    db.session.commit()

    print(student_user)


@timer
def volunteer_data():
    volunteers = list(
        map(lambda x: Volunteer(first_name="Volunteer " + str(x), last_name="Lam", username="volunteer" + str(x),
                                email=str(x) + "@gmail.com",
                                phone_number=90000000 + x,
                                password_hash=password_hash,
                                gender=GenderEnum.MALE,
                                first_name_zh_hant="志願者 " + str(x),
                                last_name_zh_hant="last_name_zh_hant",
                                dateOfBirth=date.fromisoformat('2019-12-04'),
                                _user_photo=photo_blob,
                                user_face_index="4ae75b05-22d2-41be-b881-9203534d90b0",
                                activated=True, region_id=1,
                                latitude=random_latitude(), longitude=random_longitude()),
            range(1, number_of_volunteer)))

    volunteer_user = Volunteer(first_name="Brain", last_name="Lam", username="volunteerA",
                               email="samlam020613@gmail.com",
                               phone_number=97980989,
                               password_hash=password_hash,
                               gender=GenderEnum.MALE,
                               first_name_zh_hant="志願者 X",
                               last_name_zh_hant="last_name_zh_hant",
                               dateOfBirth=date.fromisoformat('2019-12-04'),
                               activated=True, region_id=1,
                               _user_photo=photo_blob,
                               user_face_index="4ae75b05-22d2-41be-b881-9203534d90b0",
                               latitude=22.272776384977455, longitude=114.18772674351163)
    db.session.add_all([volunteer_user] + volunteers)
    db.session.commit()
    print(volunteer_user)


@timer
def donor_data():
    donors = list(
        map(lambda x: Donor(first_name="Donor " + str(x), last_name="Lam", username="Donor" + str(x),
                            email=str(x) + "_Donor@gmail.com",
                            phone_number=80000000 + x,
                            password_hash=password_hash,
                            gender=GenderEnum.MALE,
                            first_name_zh_hant="捐贈者 " + str(x),
                            last_name_zh_hant="last_name_zh_hant",
                            dateOfBirth=date.fromisoformat('2019-12-04'),
                            activated=True, region_id=1,
                            _user_photo=photo_blob,
                            user_face_index="4ae75b05-22d2-41be-b881-9203534d90b0",
                            ), range(1, number_of_donor)))

    donor_user = Donor(first_name="Brain", last_name="Lam", username="DemoDonor",
                       email="samlamsasasa@gmail.com",
                       phone_number=97980919,
                       password_hash=password_hash,
                       gender=GenderEnum.MALE,
                       first_name_zh_hant="捐贈者 X",
                       last_name_zh_hant="last_name_zh_hant",
                       dateOfBirth=date.fromisoformat('2019-12-04'),
                       activated=True, region_id=1,
                       _user_photo=photo_blob,
                       user_face_index="4ae75b05-22d2-41be-b881-9203534d90b0",
                       )
    db.session.add_all([donor_user] + donors)
    db.session.commit()
    print(donor_user)


@timer
def equipment_data():
    donors = db.session.query(Donor).all()
    equipments = []
    for donor in donors:
        equipments = list(map(
            lambda x: Equipment(description="Equipment " + str(x),
                                donor=donor,
                                status=EquipmentStatusEnum.not_selected,
                                equipment_type_id=rand.randint(1, 10),
                                _equipment_photo=photo_blob,
                                ), range(1, number_of_equipment)))
    db.session.add_all(equipments)
    db.session.commit()


@timer
def repair_applications():
    students = db.session.query(Student).all()

    for i in range(0, number_of_repair_applications_per_student):
        for student in students:
            student.repair_applications \
                .append(RepairApplication(title="title " + student.first_name,
                                          description=random_repair_details(),
                                          status=RepairApplicationStatusEnum.pending,
                                          _equipment_photo=photo_blob,
                                          latitude=random_latitude(),
                                          longitude=random_longitude(),
                                          address="address " + student.first_name,
                                          ))
    db.session.commit()


@timer
def equipment_applications():
    students = db.session.query(Student).all()

    for i in range(0, number_of_equipment_applications_per_student):
        for student in students:
            student.equipment_applications.append(EquipmentApplication(
                status=EquipmentApplicationStatusEnum.pending,
                latitude=random_latitude(),
                longitude=random_longitude(),
                address="Hoi Yuen Road, Kwun Tong",
                equipment_type_id=rand.randint(1, 10)
            ))
    db.session.commit()


def reset_person_groups():
    face_client = FaceClient(AiFaceConfig.ENDPOINT, CognitiveServicesCredentials(AiFaceConfig.KEY))
    # delete all
    # for a in face_client.person_group.list():
    #     print(a)
    #     face_client.person_group.delete(person_group_id=a.person_group_id)
    person_group_ids = set(map(lambda x: x.person_group_id, face_client.person_group.list()))

    for name, member in PersonGroupEnum.__members__.items():
        if name in person_group_ids:
            print("Delete Person Group: " + name)
            face_client.person_group.delete(person_group_id=name, name=name)
        print("Create Person Group: " + name)
        face_client.person_group.create(person_group_id=name, name=name)
        person_id = "TheDummyPerson"
        person_group_person = face_client.person_group_person.create(person_group_id=name, name=person_id)
        w = open("./data/Test Image/ID card/1.jpg", 'r+b')
        face_client.person_group_person.add_face_from_stream(name, person_group_person.person_id, w)
        face_client.person_group.train(person_group_id=name)


# the required data
with app.app_context():
    region_data()
    school_data()
    admin_data()
    teacher_data()
    student_data()
    volunteer_data()
    repair_applications()
    equipment_type_data()
    donor_data()
    equipment_data()
    equipment_applications()

reset_person_groups()
