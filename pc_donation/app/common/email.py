import inspect
import os
from os import path

import flask
from flask import current_app
from flask import render_template, url_for
from flask_babel import _
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

from app import mail, RouteConstants, TemplateConstants
from app.model.models import Teacher, Student, Admin

account_confirmation_subject = _("account verification")
repair_subject = _("repair notification")


def generate_token(field):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(field, salt=current_app.config["SECURITY_PASSWORD_SALT"])


def token_to_email(token, expiration=604800):
    try:
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        email = serializer.loads(
            token,
            salt=current_app.config["SECURITY_PASSWORD_SALT"],
            max_age=expiration
        )
    except:
        return ""
    return email


def _send_email(to, subject, data, template=TemplateConstants.Email.LOOP_ALL):
    caller = inspect.stack()[1].function
    controller = inspect.stack()[2].function
    data["caller_function"] = caller
    data["controller"] = controller
    data["tittle"] = subject

    template_file = os.path.join(os.path.dirname(__file__), "..", "templates", "email", caller + ".html")
    template_text_file = os.path.join(os.path.dirname(__file__), "..", "templates", "email", caller + "_text.html")
    current_app.logger.info(template_file)
    if path.exists(template_file) and path.exists(template_text_file):
        current_app.logger.info("Found custom template!")
        html = render_template("email/" + caller + ".html", data=data)
        text = render_template("email/" + caller + "_text.html", data=data)
    else:
        text_template = template.replace(".html", "_text.html")
        html = render_template(template, data=data)
        text = render_template(text_template, data=data)

    msg = Message(
        "iShare.support - " + subject,
        recipients=[to],
        html=html,
        body=text,
        sender=current_app.config["MAIL_DEFAULT_SENDER"]
    )
    mail.send(msg)


def message_email(to_user, from_user, message, reply_url):
    data = {
        "receiver": to_user.first_name,
        "from": from_user.first_name + " " + from_user.last_name,
        "message": message,
        "url": reply_url
    }
    _send_email(to=to_user.email, subject=_("You have a new message / 你有一條新消息"), data=data)


def thank_you_message_email_to_donor(to_user, from_user, message):
    thank_you_message_email(to_user, from_user, message, _("Thank you for your donation! / 感謝您的捐贈！"))


def thank_you_message_email_to_volunteer(to_user, from_user, message):
    thank_you_message_email(to_user, from_user, message, _("Thank you for your technical support! / 感謝您的技術支持！"))


def thank_you_message_email(to_user, from_user, message, subject):
    # TODO: Send Photo attachment.
    data = {
        "receiver": to_user.first_name,
        "from": from_user.first_name + " " + from_user.last_name,
        "message": message,
        # "photo": photo
    }
    current_app.logger.info(data)
    _send_email(to=to_user.email, subject=subject, data=data)


def password_reset_email(user):
    token = user.get_reset_password_token()
    reset_password_url = url_for(RouteConstants.NoAuthView.RESET_PASSWORD, token=token, _external=True)
    data = {
        "receiver": user.first_name,
        "url": reset_password_url
    }
    _send_email(to=user.email, subject=_("Reset Your Password / 重置你的密碼"), data=data)


def confirmation_email_address_email(user):
    user_email_token = generate_token(user.email)
    user_confirm_email_url = url_for(RouteConstants.NoAuthView.CONFIRM_EMAIL, token=user_email_token, _external=True)
    data = {
        "receiver": user.first_name,
        "url": user_confirm_email_url
    }
    _send_email(to=user.email, subject=_("Confirm your email address 請確認您的電郵地址"), data=data)


def approved_other_account_email(user):
    user_email_token = generate_token(user.email)
    if isinstance(user, Student):
        teacher_confirm_student_url = url_for(RouteConstants.TeacherView.CONFIRM_STUDENT, token=user_email_token,
                                              _external=True)
        data = {"receiver": user.teacher.first_name, "url": teacher_confirm_student_url,
                "candidate": user.first_name + " " + user.last_name}
        _send_email(to=user.teacher_email,
                    subject=_("Your student hopes you to confirm his student status / 你的學生希望你確認他的學生身份"), data=data)
    elif isinstance(user, Teacher):
        admin_confirm_teacher_url = url_for(RouteConstants.AdminView.CONFIRM_TEACHER, token=user_email_token,
                                            _external=True)
        admin = flask.g.session.query(Admin).first()
        data = {"receiver": admin.first_name, "url": admin_confirm_teacher_url,
                "candidate": user.first_name + " " + user.last_name}
        _send_email(to=admin.email, subject=_("A new teacher application / 新教師申請"), data=data)


def ask_teacher_create_account_then_approve_student_account_email(user):
    user_email_token = generate_token(user.teacher_email)
    create_teacher_account_url = url_for(RouteConstants.NoAuthView.REGISTER_TEACHER,
                                         email=user.teacher_email,
                                         token=user_email_token,
                                         _external=True)

    data = {"receiver": "Teacher", "receiver_zh": "老師", "url": create_teacher_account_url}
    _send_email(to=user.teacher_email, subject=_("Can you join us and help your student? / 你可以加入我們，幫助你的學生嗎？"),
                data=data)


def account_activated_email(user):
    data = {
        "receiver": user.first_name,
        "url": url_for(RouteConstants.NoAuthView.LOGIN, _external=True)
    }
    _send_email(to=user.email, subject=_("You account has activated. / 您的帳戶已啟動."),
                data=data)


def cancel_make_repair_application_email(repairing):
    _send_email(repairing.student.email, _("Cancellation of the repair support from volunteer."),
                _("Your repair case has been cancelled and please wait for another volunteer."))


def ask_teacher_endorse_equipment_application_email(student):
    data = {
        "receiver": student.teacher.first_name,
        "candidate": student.first_name + " " + student.last_name,
        "url": url_for(RouteConstants.TeacherView.EQUIPMENT_APPLICATION_LIST, _external=True)
    }
    _send_email(to=student.teacher.email,
                subject=_("Your student hopes you to endorse an equipment application. / 您的學生希望您認可物品申請."),
                data=data)


def approve_equipment_application_email(student):
    data = {
        "receiver": student.first_name + " " + student.last_name,
        "url": url_for(RouteConstants.HasStoryStudentView.EQUIPMENT_APPLICATION_HISTORY, _external=True)
    }
    _send_email(to=student.teacher.email,
                subject=_("Your equipment application has been approved / 您的設備申請已被批准."),
                data=data)


def reject_equipment_application_email(student):
    data = {
        "receiver": student.first_name + " " + student.last_name,
        "url": url_for(RouteConstants.HasStoryStudentView.EQUIPMENT_APPLICATION_HISTORY, _external=True)
    }
    _send_email(to=student.teacher.email,
                subject=_("Your equipment application has been rejected / 您的設備申請已被拒絕."),
                data=data)


def reject_equipment_receipts_email(donor, reason):
    data = {
        "receiver": donor.first_name + " " + donor.last_name,
        "reason": reason
    }
    _send_email(to=donor.email,
                subject=_("Your equipment receipts application has been rejected / 您的設備收據申請已被拒絕."),
                data=data)


def equipment_receipts_email(donor):
    data = {
        "receiver": donor.first_name + " " + donor.last_name,
        "url": url_for(RouteConstants.DonorView.EQUIPMENT_LIST, _external=True)
    }
    _send_email(to=donor.email,
                subject=_("Your equipment receipts application has been approved / 您的設備收據申請已被批准."),
                data=data)
