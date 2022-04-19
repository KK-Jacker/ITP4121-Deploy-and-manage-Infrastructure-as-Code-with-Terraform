import flask
from flask import current_app
from flask import redirect, url_for, flash, render_template, request
from flask_babel import _, get_locale
from flask_classful import route
from flask_login import current_user

from app.common.base_flask_view import BaseFlaskView
from app.common.decorator import is_teacher
from app.common.email import token_to_email, account_activated_email, approve_equipment_application_email, \
    reject_equipment_application_email
from app.model.models import Student, EquipmentApplication
from app.model.status_enum import StudentStatusEnum, EquipmentApplicationStatusEnum
from app.route_constants import RouteConstants
from app.teacher.forms import ConfirmStudentForm
from app.template_constants import TemplateConstants
from config import AiChatbotConfig, Config
from app.static_function import PageSet



class TeacherView(BaseFlaskView):
    route_base = "teacher"
    decorators = [is_teacher]

    def index(self):
        
        lang = str(get_locale())

        return render_template(TemplateConstants.Teacher.INDEX, title=_("Teacher View"),
                               lang=lang,
                               key=AiChatbotConfig.teacher_chatbot_key)

    @route("/confirm-student/<token>", methods=["GET", "POST"])
    def confirm_student(self, token):
        student_email = token_to_email(token)
        if student_email:
            student = flask.g.session.query(Student).filter_by(email=student_email).filter_by(
                teacher_email=current_user.email).first()
            return self._confirm_student(student)
        else:
            flash(_("The confirmation link is invalid or has expired."), "danger")
            return redirect(url_for(RouteConstants.TeacherView.TEACHER_APPROVED_STUDENT_LIST))

    @route("/teacher-approved-student/<student_id>", methods=["GET", "POST"])
    def teacher_approved_student(self, student_id: int):
        student = flask.g.session.query(Student).filter_by(
            id=student_id).filter_by(school=current_user.school).first()
        return self._confirm_student(student)

    @staticmethod
    def _confirm_student(student):
        form = ConfirmStudentForm(obj=student)
        form.school_name.data = student.school.name_en
        form.school_URL.data = student.school.url
        if form.validate_on_submit():
            if form.approve:
                current_app.logger.info(student.teacher)
                student.teacher = current_user
                if student.status == StudentStatusEnum.activated:
                    flash(_("Approved"))
                elif student.status == StudentStatusEnum.not_activated:
                    student.status = StudentStatusEnum.student_not_activated_and_teacher_approved
                    flash(_("student_not_activated_and_teacher_approved"))
                elif student.status == StudentStatusEnum.student_activated_wait_for_teacher_approval:
                    student.status = StudentStatusEnum.activated
                    flash(_("Student activated"))
                    account_activated_email(student)
                flask.g.session.commit()
            else:
                flash(_("The confirmation link is invalid or has expired."), "danger")
            return redirect(url_for(RouteConstants.TeacherView.TEACHER_APPROVED_STUDENT_LIST))
        return render_template(TemplateConstants.Teacher.TEACHER_CONFIRM, title=_("Approve Student Form"), form=form,
                               student=student)

    def teacher_approved_student_list(self):
        page = request.args.get('page', default=1, type=int)
        last_student = flask.g.session.query(Student).filter_by(school=current_user.school).filter_by(
            teacher_email=current_user.email).count()
        paging = PageSet(page,Config.PAGING_PER_PAGE,last_student)
        student_data = flask.g.session.query(Student).filter_by(school=current_user.school).filter_by(
            teacher_email=current_user.email).slice(paging.item_start, paging.item_end)
        return render_template(TemplateConstants.Teacher.TEACHER_APPROVED_STUDENT_RECORD,
                               title=_("Teacher Approved Student Record"),
                               records=student_data, StudentStatusEnum=StudentStatusEnum, page=page, last_page=paging.last_page,
                               page_list=paging.page_list)

    def equipment_application_list(self):
        equipment_applications = flask.g.session.query(EquipmentApplication) \
            .join(Student).filter(Student.teacher == current_user).all()
        current_app.logger.info(equipment_applications)
        return render_template(TemplateConstants.Teacher.EQUIPMENT_APPLICATION_LIST,
                               title=_("Teacher approved Student's Equipment Application Record"),
                               records=equipment_applications,
                               EquipmentApplicationStatusEnum=EquipmentApplicationStatusEnum)

    @route("/approve-equipment-application/<equipment_application_id>", methods=["GET", "POST"])
    def approve_equipment_application(self, equipment_application_id: int):
        student = self._update_equipment_application_by_id(equipment_application_id,
                                                           EquipmentApplicationStatusEnum.pending)
        approve_equipment_application_email(student)
        flask.g.session.commit()
        return redirect(url_for(RouteConstants.TeacherView.EQUIPMENT_APPLICATION_LIST))

    @route("/reject-equipment-application/<equipment_application_id>", methods=["GET", "POST"])
    def reject_equipment_application(self, equipment_application_id: int):
        student = self._update_equipment_application_by_id(equipment_application_id,
                                                           EquipmentApplicationStatusEnum.teacher_rejected)
        reject_equipment_application_email(student)
        flask.g.session.commit()
        return redirect(url_for(RouteConstants.TeacherView.EQUIPMENT_APPLICATION_LIST))

    @staticmethod
    def _update_equipment_application_by_id(equipment_application_id, status):
        equipment_application = flask.g.session.query(EquipmentApplication).join(Student).filter(
            EquipmentApplication.id == equipment_application_id) \
            .filter(Student.teacher == current_user).first()
        equipment_application.status = status
        return equipment_application.student
