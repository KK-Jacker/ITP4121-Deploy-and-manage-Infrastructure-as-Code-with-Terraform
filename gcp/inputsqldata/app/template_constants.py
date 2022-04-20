class TemplateConstants:
    _POST = "_post.html"
    ABOUT_US = "about_us.html"
    BASE = "base.html"
    EDIT_PROFILE = "edit_profile.html"
    INDEX = "index.html"
    INIT = "init.html"
    MESSAGE = "message.html"
    SUPPORTERS = "supporters.html"
    TERMS = "terms.html"
    USER = "user.html"

    class Admin:
        CONFIRM_TEACHER = "admin/confirm_teacher.html"
        DONATION_LIST = "admin/donation_list.html"
        INDEX = "admin/index.html"
        TEACHER_LIST = "admin/teacher_list.html"
        VERIFY_RECEIPTS = "admin/verify_receipts.html"

        

    class Auth:
        LOGIN = "auth/login.html"
        REGISTER_FIRST_PAGE = "auth/register_first_page.html"
        REGISTER_FIRST_PAGE_WITH_AUTO_FILL_IN = "auth/register_first_page_with_auto_fill_in.html"
        REGISTER_STUDENT_SECOND_PAGE = "auth/register_student_second_page.html"
        REGISTER_TEACHER_SECOND_PAGE = "auth/register_teacher_second_page.html"
        REGISTER_VOLUNTEER_SECOND_PAGE = "auth/register_volunteer_second_page.html"
        RESEND_CONFIRMATION_EMAIL = "auth/resend_confirmation_email.html"
        RESET_PASSWORD = "auth/reset_password.html"
        RESET_PASSWORD_REQUEST = "auth/reset_password_request.html"

    class Donor:
        DONATE_EQUIPMENT = "donor/donate_equipment.html"
        DONATE_EQUIPMENT_TO_STUDENT = "donor/donate_equipment_to_student.html"
        EQUIPMENT_APPLICATIONS_MAP = "donor/equipment_applications_map.html"
        EQUIPMENT_LIST = "donor/equipment_list.html"
        INDEX = "donor/index.html"

    class Email:
        ACCOUNT_ACTIVATED_EMAIL = "email/account_activated_email.html"
        ACCOUNT_ACTIVATED_EMAIL_TEXT = "email/account_activated_email_text.html"
        APPROVE_EQUIPMENT_APPLICATION_EMAIL = "email/approve_equipment_application_email.html"
        APPROVE_EQUIPMENT_APPLICATION_EMAIL_TEXT = "email/approve_equipment_application_email_text.html"
        APPROVED_OTHER_ACCOUNT_EMAIL = "email/approved_other_account_email.html"
        APPROVED_OTHER_ACCOUNT_EMAIL_TEXT = "email/approved_other_account_email_text.html"
        ASK_TEACHER_CREATE_ACCOUNT_THEN_APPROVE_STUDENT_ACCOUNT_EMAIL = "email/ask_teacher_create_account_then_approve_student_account_email.html"
        ASK_TEACHER_CREATE_ACCOUNT_THEN_APPROVE_STUDENT_ACCOUNT_EMAIL_TEXT = "email/ask_teacher_create_account_then_approve_student_account_email_text.html"
        ASK_TEACHER_ENDORSE_EQUIPMENT_APPLICATION_EMAIL = "email/ask_teacher_endorse_equipment_application_email.html"
        ASK_TEACHER_ENDORSE_EQUIPMENT_APPLICATION_EMAIL_TEXT = "email/ask_teacher_endorse_equipment_application_email_text.html"
        CONFIRMATION_EMAIL_ADDRESS_EMAIL = "email/confirmation_email_address_email.html"
        CONFIRMATION_EMAIL_ADDRESS_EMAIL_TEXT = "email/confirmation_email_address_email_text.html"
        Layouts_EMAIL = "email/layouts/email.html"
        Layouts_EMAIL_TEXT = "email/layouts/email_text.html"
        LOOP_ALL = "email/loop_all.html"
        LOOP_ALL_TEXT = "email/loop_all_text.html"
        MESSAGE_EMAIL = "email/message_email.html"
        MESSAGE_EMAIL_TEXT = "email/message_email_text.html"
        PASSWORD_RESET_EMAIL = "email/password_reset_email.html"
        PASSWORD_RESET_EMAIL_TEXT = "email/password_reset_email_text.html"
        REJECT_EQUIPMENT_APPLICATION_EMAIL = "email/reject_equipment_application_email.html"
        REJECT_EQUIPMENT_APPLICATION_EMAIL_TEXT = "email/reject_equipment_application_email_text.html"
        THANK_YOU_MESSAGE_EMAIL = "email/thank_you_message_email.html"
        THANK_YOU_MESSAGE_EMAIL_TEXT = "email/thank_you_message_email_text.html"

    class Errors:
        STATUS_404 = "errors/status_404.html"
        STATUS_500 = "errors/status_500.html"

    class Student:
        CREATE_EQUIPMENT_APPLICATION = "student/create_equipment_application.html"
        EDIT_REPAIR_APPLICATION = "student/edit_repair_application.html"
        EQUIPMENT_APPLICATION_HISTORY = "student/equipment_application_history.html"
        EQUIPMENT_APPLICATION_MAP = "student/equipment_application_map.html"
        INDEX = "student/index.html"
        REPAIR_APPLICATION = "student/repair_application.html"
        REPAIR_APPLICATION_LIST = "student/repair_application_list.html"
        STORY = "student/story.html"
        THANK_YOU = "student/thank_you.html"

    class Teacher:
        EQUIPMENT_APPLICATION_LIST = "teacher/equipment_application_list.html"
        INDEX = "teacher/index.html"
        TEACHER_APPLY = "teacher/teacher_apply.html"
        TEACHER_APPROVED_STUDENT_RECORD = "teacher/teacher_approved_student_record.html"
        TEACHER_CONFIRM = "teacher/teacher_confirm.html"

    class Volunteer:
        INDEX = "volunteer/index.html"
        REPAIR_APPLICATION = "volunteer/repair_application.html"
        VOLUNTEER_CHOOSE_REPAIR_EQUIPMENT_CASE = "volunteer/volunteer_choose_repair_equipment_case.html"
        VOLUNTEER_RECORD = "volunteer/volunteer_record.html"
