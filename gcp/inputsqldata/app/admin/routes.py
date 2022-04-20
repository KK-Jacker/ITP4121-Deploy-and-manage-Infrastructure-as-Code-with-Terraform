import flask
from flask import redirect, url_for, flash, render_template, request
from flask_babel import _, get_locale
from flask_classful import route
from flask_login import current_user
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from app.admin.forms import ConfirmTeacherForm, VerifyReceiptForm
from app.common.base_flask_view import BaseFlaskView
from app.common.decorator import is_admin
from app.common.email import token_to_email, confirmation_email_address_email, account_activated_email, \
    reject_equipment_receipts_email, equipment_receipts_email
from app.model.models import Teacher, EquipmentApplication, Equipment
from app.model.status_enum import TeacherStatusEnum, EquipmentApplicationStatusEnum
from app.route_constants import RouteConstants
from app.template_constants import TemplateConstants

from app.length_constants import LengthConstant
from app.static_function import PageSet
from config import Config


class AdminView(BaseFlaskView):
    route_base = "admin"
    decorators = [is_admin]

    def index(self):
        lang = str(get_locale())

        return render_template(TemplateConstants.Admin.INDEX, title=_("Admin View"),
                               lang=lang)

    def teacher_list(self):
        page = request.args.get('page', default=1, type=int)
        last_teacher = flask.g.session.query(Teacher).count()
        paging = PageSet(page,Config.PAGING_PER_PAGE,last_teacher)
        teacher_data = flask.g.session.query(Teacher).order_by(Teacher.id.desc()).slice(paging.item_start, paging.item_end)
        return render_template(TemplateConstants.Admin.TEACHER_LIST,
                               title=_("Teacher List"),
                               teachers=teacher_data, TeacherStatusEnum=TeacherStatusEnum, page=page, last_page=paging.last_page, page_list=paging.page_list)



    @route("/approve-teacher/<teacher_id>", methods=["GET", "POST"])
    def approve_teacher(self, teacher_id: int):
        teacher = flask.g.session.query(Teacher).filter(
            Teacher.id == teacher_id).first()
        return self._confirm_teacher(teacher)

    @route("/confirm-teacher/<token>", methods=["GET", "POST"])
    def confirm_teacher(self, token):
        teacher_email = token_to_email(token)
        if teacher_email:
            teacher = flask.g.session.query(Teacher).filter_by(email=teacher_email).first()
            return self._confirm_teacher(teacher)
        else:
            flash(_("The confirmation link is invalid or has expired."), "danger")
            return redirect(url_for(RouteConstants.AdminView.TEACHER_LIST))

    @staticmethod
    def _confirm_teacher(teacher):
        form = ConfirmTeacherForm(obj=teacher)
        form.school_name.data = teacher.school.name_en
        form.school_URL.data = teacher.school.url
        if form.validate_on_submit():
            if form.approve.data:
                teacher.admin = current_user
                if teacher.status == TeacherStatusEnum.activated:
                    flash(_("You have activated this teacher account."))
                elif teacher.status == TeacherStatusEnum.not_activated:
                    flash(_("Emailed the teacher to confirm account."))
                    teacher.status = TeacherStatusEnum.teacher_not_activated_and_admin_approved
                    confirmation_email_address_email(teacher)
                elif teacher.status == TeacherStatusEnum.teacher_activated_wait_for_admin_approval:
                    teacher.status = TeacherStatusEnum.activated
                    account_activated_email(teacher)
                    flash(_("You have activated a teacher account - ") + teacher.email)
                flask.g.session.commit()
            else:
                teacher.status = TeacherStatusEnum.admin_rejected
                flash(_("You have rejected this teacher account."))
            return redirect(url_for(RouteConstants.AdminView.TEACHER_LIST))
        return render_template(TemplateConstants.Admin.CONFIRM_TEACHER, title=_("confirm form"), form=form,
                               teacher=teacher)

    def donation_list(self):
        applications = flask.g.session.query(EquipmentApplication).join(Equipment).options(
            joinedload(EquipmentApplication.donor)).options(
            joinedload(EquipmentApplication.equipment).subqueryload(Equipment.equipment_type)).filter(
            and_(EquipmentApplication.status == EquipmentApplicationStatusEnum.donated_waiting_for_receipt,
                 Equipment.has_receipt.is_(True)
                 )
        ).order_by(EquipmentApplication.updated_at.desc())
        return render_template(TemplateConstants.Admin.DONATION_LIST,
                               title=_("Admin Approved Teacher record"),
                               applications=applications, TeacherStatusEnum=TeacherStatusEnum)

    @route("/verify-receipts/<equipment_application_id>", methods=["GET", "POST"])
    def verify_receipts(self, equipment_application_id: int):
        equipment_application = flask.g.session.query(EquipmentApplication).filter(
            EquipmentApplication.id == equipment_application_id).first()
        equipment = equipment_application.equipment
        form = VerifyReceiptForm(obj=equipment)

        thanks_photo_url = equipment_application.thanks_photo
        # match_student = is_face_present(PersonGroupEnum.student, thanks_photo_url,
        #                                 [equipment_application.student.user_type_face_index])
        # match_donor = is_face_present(PersonGroupEnum.donor, thanks_photo_url,
        #                               [equipment.donor.user_type_face_index])
        # match_donor_student = is_face_present(PersonGroupEnum.all, thanks_photo_url,
        #                                       [equipment_application.student.user_face_index,
        #                                        equipment.donor.user_face_index])

        # current_app.logger.info(match_student, match_donor, match_donor_student)
        # face_match = {_("Match Student"): match_student, _("Match Donor"): match_donor,
        #               _("Match Donor and Student"): match_donor_student}
        if form.validate_on_submit():
            if form.reject.data:
                form.populate_obj(equipment)
                equipment_application.status = EquipmentApplicationStatusEnum.completed_receipt_rejected
                reject_equipment_receipts_email(equipment_application.donor, equipment.receipt_reject_reason)
                flash(_("Reject message sent to ") + equipment_application.donor.email)
                flask.g.session.commit()
            elif form.approve.data:
                form.populate_obj(equipment)
                equipment_application.status = EquipmentApplicationStatusEnum.completed_with_receipt
                equipment_application.equipment.admin = current_user
                equipment_receipts_email(equipment_application.donor)
                flash(_("Receipts sent to ") + equipment_application.donor.email)
                flask.g.session.commit()
            return redirect(url_for(RouteConstants.AdminView.DONATION_LIST))
        return render_template(TemplateConstants.Admin.VERIFY_RECEIPTS,
                               title=_("Admin Verify Donation Receipt"),
                               form=form,
                               # face_match=face_match,
                               equipment_application=equipment_application)
