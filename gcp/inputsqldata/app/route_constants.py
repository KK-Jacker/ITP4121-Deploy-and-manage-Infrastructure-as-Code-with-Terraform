class RouteConstants:
    STATIC = "static"

    class AdminView:
        APPROVE_TEACHER = "AdminView:approve_teacher"
        CONFIRM_TEACHER = "AdminView:confirm_teacher"
        DONATION_LIST = "AdminView:donation_list"
        INDEX = "AdminView:index"
        TEACHER_LIST = "AdminView:teacher_list"
        VERIFY_RECEIPTS = "AdminView:verify_receipts"

    class AuthView:
        LOGOUT = "AuthView:logout"
        RESEND_CONFIRMATION_EMAIL = "AuthView:resend_confirmation_email"
        SCHOOL_JSON = "AuthView:school_json"

    class Bootstrap:
        STATIC = "bootstrap.static"

    class DonorView:
        CANCEL_DONATION = "DonorView:cancel_donation"
        DELETE_DONATED_EQUIPMENT = "DonorView:delete_donated_equipment"
        DONATE_EQUIPMENT = "DonorView:donate_equipment"
        DONATE_EQUIPMENT_MAP = "DonorView:donate_equipment_map"
        DONATE_EQUIPMENT_TO_STUDENT = "DonorView:donate_equipment_to_student"
        DOWNLOAD_EQUIPMENT_RECEIPTS = "DonorView:download_equipment_receipts"
        EQUIPMENT_APPLICATION_CASE_JSON = "DonorView:equipment_application_case_json"
        EQUIPMENT_LIST = "DonorView:equipment_list"
        INDEX = "DonorView:index"
        MSG_TO_STUDENT = "DonorView:msg_to_student"

    class HasStoryStudentView:
        CANCEL_REQUESTED_EQUIPMENT_APPLICATION = "HasStoryStudentView:cancel_requested_equipment_application"
        COMPLETE_EQUIPMENT_APPLICATION = "HasStoryStudentView:complete_equipment_application"
        CREATE_EQUIPMENT_APPLICATION = "HasStoryStudentView:create_equipment_application"
        DELETE_REPAIR_APPLICATION = "HasStoryStudentView:delete_repair_application"
        EDIT_REPAIR_APPLICATION = "HasStoryStudentView:edit_repair_application"
        EQUIPMENT_APPLICATION_HISTORY = "HasStoryStudentView:equipment_application_history"
        EQUIPMENT_APPLICATION_MAP = "HasStoryStudentView:equipment_application_map"
        MSG_TO_DONOR = "HasStoryStudentView:msg_to_donor"
        MSG_TO_VOLUNTEER = "HasStoryStudentView:msg_to_volunteer"
        NEW_REPAIR_APPLICATION = "HasStoryStudentView:new_repair_application"
        REPAIR_APPLICATION = "HasStoryStudentView:repair_application"
        REPAIR_APPLICATION_LIST = "HasStoryStudentView:repair_application_list"
        STUDENT_COMPLETE_REPAIR_EQUIPMENT = "HasStoryStudentView:student_complete_repair_equipment"
        THANKS_TO_DONOR_COMPLETE_EQUIPMENT_APPLICATION = "HasStoryStudentView:thanks_to_donor_complete_equipment_application"
        THANKS_TO_VOLUNTEER_COMPLETE_REPAIR_EQUIPMENT = "HasStoryStudentView:thanks_to_volunteer_complete_repair_equipment"

    class MainView:
        ABOUT_US = "MainView:about_us"
        EDIT_PROFILE = "MainView:edit_profile"
        INDEX = "MainView:index"
        LANGUAGE = "MainView:language"
        SUPPORTERS = "MainView:supporters"
        TERMS = "MainView:terms"
        USER = "MainView:user"

    class NoAuthView:
        CONFIRM_EMAIL = "NoAuthView:confirm_email"
        LOGIN = "NoAuthView:login"
        REGISTER_DONOR = "NoAuthView:register_donor"
        REGISTER_STUDENT = "NoAuthView:register_student"
        REGISTER_STUDENT_SECOND_PAGE = "NoAuthView:register_student_second_page"
        REGISTER_TEACHER = "NoAuthView:register_teacher"
        REGISTER_TEACHER_SECOND_PAGE = "NoAuthView:register_teacher_second_page"
        REGISTER_VOLUNTEER = "NoAuthView:register_volunteer"
        REGISTER_VOLUNTEER_SECOND_PAGE = "NoAuthView:register_volunteer_second_page"
        RESET_PASSWORD = "NoAuthView:reset_password"
        RESET_PASSWORD_REQUEST = "NoAuthView:reset_password_request"

    class StudentView:
        EDIT_STORY = "StudentView:edit_story"
        INDEX = "StudentView:index"
        STORY = "StudentView:story"

    class TeacherView:
        APPROVE_EQUIPMENT_APPLICATION = "TeacherView:approve_equipment_application"
        CONFIRM_STUDENT = "TeacherView:confirm_student"
        EQUIPMENT_APPLICATION_LIST = "TeacherView:equipment_application_list"
        INDEX = "TeacherView:index"
        REJECT_EQUIPMENT_APPLICATION = "TeacherView:reject_equipment_application"
        TEACHER_APPROVED_STUDENT = "TeacherView:teacher_approved_student"
        TEACHER_APPROVED_STUDENT_LIST = "TeacherView:teacher_approved_student_list"

    class VolunteerView:
        CANCEL_MAKE_REPAIR_APPLICATION = "VolunteerView:cancel_make_repair_application"
        CREATE_REPAIR_APPLICATION = "VolunteerView:create_repair_application"
        EDIT_REPAIR_APPLICATION = "VolunteerView:edit_repair_application"
        INDEX = "VolunteerView:index"
        MSG_TO_STUDENT = "VolunteerView:msg_to_student"
        REPAIR_CASE_JSON = "VolunteerView:repair_case_json"
        VOLUNTEER_RECORD = "VolunteerView:volunteer_record"
        VOLUNTEER_REPAIR_ITEM_CASE = "VolunteerView:volunteer_repair_item_case"
