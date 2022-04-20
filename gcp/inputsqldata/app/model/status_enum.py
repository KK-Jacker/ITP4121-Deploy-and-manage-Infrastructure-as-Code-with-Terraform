import enum
from flask_babel import lazy_gettext as _l


class BaseEnum(enum.Enum):
    @classmethod
    def get_name_to_value_dict(cls):
        role_names = dict([(cls.__name__ + "." + role, member.value) for role, member in cls.__members__.items()])
        return role_names

    @classmethod
    def get_value_to_name_dict(cls):
        role_names = dict([(member.value, cls.__name__ + "." + role) for role, member in cls.__members__.items()])
        return role_names


# https://stackoverflow.com/questions/43160780/python-flask-wtform-selectfield-with-enum-values-not-a-valid-choice-upon-valid
class FormEnum(enum.IntEnum):
    @classmethod
    def choices(cls):
        # return [-1, _l('Please Select')] + [(choice, choice.name) for choice in cls]
        return  [(choice, choice.name) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(int(item)) if not isinstance(item, cls) else item

    def __str__(self):
        return str(self.value)


class StudentStatusEnum(BaseEnum):
    not_activated = 1
    student_activated_wait_for_teacher_approval = 2
    student_not_activated_and_teacher_approved = 3
    activated = 4


class TeacherStatusEnum(BaseEnum):
    not_activated = 1
    teacher_activated_wait_for_admin_approval = 2
    teacher_not_activated_and_admin_approved = 3
    admin_rejected = 4
    activated = 5


class EquipmentStatusEnum(BaseEnum):
    not_selected = 1
    selected = 2
    pending = 3
    completed = 4


class EquipmentApplicationStatusEnum(BaseEnum):
    waiting_for_teacher_approval = 1
    teacher_rejected = 2
    pending = 3
    in_progress = 4
    donated = 5
    completed_without_receipt = 6
    donated_waiting_for_receipt = 7
    completed_with_receipt = 8
    completed_receipt_rejected = 9


class RepairApplicationStatusEnum(BaseEnum):
    pending = 1
    repairing = 2
    repaired = 3
    completed = 4


class SchoolCategoryEnum(BaseEnum):
    AIDED_PRIMARY_SCHOOLS = 1
    AIDED_SECONDARY_SCHOOLS = 2
    AIDED_SPECIAL_SCHOOLS = 3
    CAPUT_SECONDARY_SCHOOLS = 4
    DIRECT_SUBSIDY_SCHEME_PRIMARY_SCHOOLS = 5
    DIRECT_SUBSIDY_SCHEME_SECONDARY_SCHOOLS = 6
    ENGLISH_SCHOOLS_FOUNDATION_PRIMARY = 7
    ENGLISH_SCHOOLS_FOUNDATION_SECONDARY = 8
    GOVERNMENT_PRIMARY_SCHOOLS = 9
    GOVERNMENT_SECONDARY_SCHOOLS = 10
    INTERNATIONAL_SCHOOLS_PRIMARY = 11
    INTERNATIONAL_SCHOOLS_SECONDARY = 12
    KINDERGARTEN_CUM_CHILD_CARE_CENTRES = 13
    KINDERGARTENS = 14
    PRIVATE_PRIMARY_SCHOOLS = 15
    PRIVATE_SECONDARY_SCHOOLS_DAY_EVENING = 16


class GenderEnum(FormEnum):
    MALE = 1
    FEMALE = 2
