import io
import json
from datetime import datetime

import flask
from flask import current_app
from flask import redirect, url_for, flash, request, render_template, jsonify, send_file
from flask_babel import _, get_locale
from flask_classful import route
from flask_login import current_user
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from app.common.base_flask_view import BaseFlaskView
from app.common.decorator import is_donor
from app.common.email import message_email
from app.common.form import get_msg_form
from app.common.form_helper import populate_form_equipment_types
from app.donor import index_data
from app.donor.forms import DonateEquipmentForm, DonateConfirmForm
from app.model.models import Equipment, EquipmentApplication, Student, Story, \
    Message
from app.model.status_enum import EquipmentStatusEnum, EquipmentApplicationStatusEnum
from app.route_constants import RouteConstants
from app.template_constants import TemplateConstants
from config import GoogleMapConfig, AiChatbotConfig, Config
from app.static_function import PageSet

now = datetime.now()
current_time = now.strftime("%H_%M_%S")


class DonorView(BaseFlaskView):
    route_base = "donor"
    decorators = [is_donor]

    # main page of donor
    def index(self):
        lang = str(get_locale())
        # TODO: Will need to support zh_TW
        return render_template(TemplateConstants.Donor.INDEX, title=_("Donor View"), lang=lang,
                               key=AiChatbotConfig.donor_chatbot_key,
                               )

    @route("/donate-equipment/", methods=["GET", "POST"])
    def donate_equipment(self):
        form = DonateEquipmentForm()

        '''equipments = flask.g.session.query(Equipment).filter(
            and_(Equipment.donor == current_user, Equipment.status == EquipmentStatusEnum.not_selected)).order_by(
            Equipment.created_at.desc())'''
        page = request.args.get('page', default=1, type=int)
        last_item = flask.g.session.query(Equipment).filter(
            and_(Equipment.donor == current_user)).count()
        paging = PageSet(page, Config.PAGING_PER_PAGE, last_item)
        equipments = flask.g.session.query(Equipment).filter(
            and_(Equipment.donor == current_user, Equipment.status == EquipmentStatusEnum.not_selected)).order_by(
            Equipment.created_at.desc()).slice(paging.item_start, paging.item_end)
        populate_form_equipment_types(form)
        if form.validate_on_submit():
            equipment = Equipment()
            equipment.donor = current_user
            equipment.status = EquipmentStatusEnum.not_selected
            form.populate_obj(equipment)
            flask.g.session.add(equipment)
            flask.g.session.commit()
            flash(_("Your equipment has added for donation."))
            return redirect(url_for(RouteConstants.DonorView.DONATE_EQUIPMENT))
        return render_template(TemplateConstants.Donor.DONATE_EQUIPMENT, form=form, equipments=equipments, page=page, last_page=paging.last_page, page_list=paging.page_list)

    def delete_donated_equipment(self, equipment_id: int):
        current_app.logger.info(equipment_id)
        donated_equipment = flask.g.session.query(Equipment).filter(
            and_(
                Equipment.donor == current_user,
                Equipment.status == EquipmentStatusEnum.not_selected,
                Equipment.id == equipment_id
            )).first()
        if donated_equipment is None:
            return render_template(TemplateConstants.Errors.STATUS_404), 404
        flask.g.session.delete(donated_equipment)
        flask.g.session.commit()
        # Back to previous page.
        return redirect(request.referrer)

    def equipment_list(self):
        '''equipments = flask.g.session.query(Equipment).outerjoin(EquipmentApplication).filter(
            Equipment.donor == current_user).order_by(
            Equipment.created_at.desc())'''
        page = request.args.get('page', default=1, type=int)
        last_item = flask.g.session.query(Equipment).filter(
            and_(Equipment.donor == current_user)).count()
        paging = PageSet(page, Config.PAGING_PER_PAGE, last_item)
        equipments = flask.g.session.query(Equipment).outerjoin(EquipmentApplication).filter(
            Equipment.donor == current_user).order_by(
            Equipment.created_at.desc()).slice(paging.item_start, paging.item_end)
        return render_template(TemplateConstants.Donor.EQUIPMENT_LIST, equipments=equipments,
                               EquipmentStatusEnum=EquipmentStatusEnum,
                               EquipmentApplicationStatusEnum=EquipmentApplicationStatusEnum, page=page, last_page=paging.last_page, page_list=paging.page_list)

    def donate_equipment_map(self, equipment_id: int):
        equipment = flask.g.session.query(Equipment).filter(
            and_(
                Equipment.donor == current_user,
                Equipment.status == EquipmentStatusEnum.not_selected,
                Equipment.id == equipment_id
            )).first()
        equipment = {"id": equipment.id, "description": equipment.description,
                     "equipment_type_id": equipment.equipment_type_id,
                     "photo_url": equipment.equipment_photo}
        return render_template(TemplateConstants.Donor.EQUIPMENT_APPLICATIONS_MAP,
                               title=_("Pick A Student"),
                               equipment=equipment,
                               key=GoogleMapConfig.KEY)

    def equipment_application_case_json(self, equipment_id: int):
        bound = json.loads(request.args.get("bound"))
        additional_filter = json.loads(request.args.get("additionalFilter"))
        language = additional_filter["language"]
        equipment = flask.g.session.query(Equipment).filter(
            and_(
                Equipment.donor == current_user,
                Equipment.status == EquipmentStatusEnum.not_selected,
                Equipment.id == equipment_id
            )).first()
        applications = flask.g.session.query(EquipmentApplication).join(Student).join(
            Story).options(
            joinedload(EquipmentApplication.student).subqueryload(Student.story)).filter(
            and_(
                EquipmentApplication.latitude < bound["north"],
                EquipmentApplication.latitude > bound["south"],
                EquipmentApplication.longitude < bound["east"],
                EquipmentApplication.longitude > bound["west"],
                EquipmentApplication.status == EquipmentApplicationStatusEnum.pending,
                EquipmentApplication.equipment_type == equipment.equipment_type
            )).order_by(
            Story.urgency.desc())

        applications = list(applications)
        number_of_case = len(applications)
        ranks = [sorted(applications, key=lambda a: a.student.story.urgency).index(x) + 1 for x in applications]
        max_rank = max(max(ranks), 1)
        data = [{"id": a.id,
                 "latitude": a.latitude,
                 "longitude": a.longitude,
                 "title": a.student.story.title_en if language == "en" else a.student.story.title_zh_Hant,
                 "description": a.student.story.content_en if language == "en" else a.student.story.content_zh_Hant,
                 "created_at": a.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
                 "image": a.student.story.story_photo,
                 "url": url_for(RouteConstants.DonorView.DONATE_EQUIPMENT_TO_STUDENT,
                                equipment_id=equipment_id,
                                equipment_application_id=a.id),
                 "urgency": a.student.story.urgency,
                 "opacity": max(0.1, ranks[i] / max_rank)} for i, a in enumerate(applications)]

        if number_of_case == 0:
            return {"status": "ok", "data": []}
        if number_of_case > 500:
            return {"status": _("More than 500 records found, and please zoom in!"), "data": []}
        return jsonify({"status": "ok", "data": data})

    @route("/donate-equipment-to-student/<equipment_id>/<equipment_application_id>", methods=["GET", "POST"])
    def donate_equipment_to_student(self, equipment_id: int, equipment_application_id: int):
        equipment = flask.g.session.query(Equipment).filter(
            and_(
                Equipment.donor == current_user,
                Equipment.status == EquipmentStatusEnum.not_selected,
                Equipment.id == equipment_id
            )).first()
        equipment_application = flask.g.session.query(EquipmentApplication).join(Student).join(Story).options(
            joinedload(EquipmentApplication.student).subqueryload(Student.story)).filter(
            and_(
                EquipmentApplication.id == equipment_application_id,
                EquipmentApplication.status == EquipmentApplicationStatusEnum.pending
            )).first()

        if equipment is None:
            flash(_("This equipment has been donated to another student."))
            return redirect(url_for(RouteConstants.DonorView.INDEX))
        form = DonateConfirmForm()
        if form.validate_on_submit():
            equipment_application.donor = current_user
            equipment_application.time = form.date_time.data
            equipment_application.status = EquipmentApplicationStatusEnum.in_progress
            equipment.equipment_application = equipment_application
            equipment.status = EquipmentStatusEnum.selected

            message_to_student = Message()
            message_to_student.message = _(
                "Hello, I decide to donate my equipment to you. It is ") + equipment_application.equipment.equipment_type.name
            message_to_student.equipment_application = equipment_application
            message_to_student.from_student = False

            reply_url = url_for(RouteConstants.HasStoryStudentView.MSG_TO_DONOR,
                                equipment_application_id=equipment_application.id,
                                _external=True)
            message_email(equipment_application.student, equipment_application.donor, message_to_student.message,
                          reply_url)

            message_to_donor = Message()
            message_to_donor.message = _("Thank you!")
            message_to_donor.equipment_application = equipment_application
            message_to_donor.from_student = True

            reply_url = url_for(RouteConstants.DonorView.MSG_TO_STUDENT,
                                equipment_application_id=equipment_application.id,
                                _external=True)
            message_email(equipment_application.donor, equipment_application.student, message_to_donor.message,
                          reply_url)

            flask.g.session.add(message_to_student)
            flask.g.session.add(message_to_donor)
            flask.g.session.commit()

            flash(_("Donation Appointment has made!"))
            return redirect(url_for(RouteConstants.DonorView.EQUIPMENT_LIST))
        return render_template(TemplateConstants.Donor.DONATE_EQUIPMENT_TO_STUDENT, equipment=equipment, form=form,
                               equipment_application=equipment_application, key=GoogleMapConfig.KEY)

    @route("/cancel-donation/<equipment_application_id>", methods=["GET", "POST"])
    def cancel_donation(self, equipment_application_id: int):
        equipment_application = flask.g.session.query(EquipmentApplication).join(Equipment).join(Student).filter(
            and_(
                EquipmentApplication.donor == current_user,
                EquipmentApplication.id == equipment_application_id,
                EquipmentApplication.status == EquipmentApplicationStatusEnum.in_progress
            )).first()
        equipment_application.donor = None
        equipment_application.time = None
        equipment_application.status = EquipmentApplicationStatusEnum.pending
        equipment_application.equipment.status = EquipmentStatusEnum.not_selected
        equipment_application.equipment = None
        flask.g.session.commit()
        return redirect(url_for(RouteConstants.DonorView.EQUIPMENT_LIST))

    @route("/msg-to-student/<equipment_application_id>", methods=["GET", "POST"])
    def msg_to_student(self, equipment_application_id: int):
        equipment_application = flask.g.session.query(EquipmentApplication).filter(
            and_(
                EquipmentApplication.donor == current_user,
                EquipmentApplication.id == equipment_application_id,
                EquipmentApplication.status == EquipmentApplicationStatusEnum.in_progress
            )).first()

        if equipment_application is None or equipment_application.messages is None:
            return redirect(url_for(RouteConstants.DonorView.EQUIPMENT_LIST))

        messages = equipment_application.messages.order_by(Message.created_at.desc())
        form = get_msg_form(messages)
        messages = list(map(lambda m: {"from_student": m.from_student, "message": m.message,
                                       "other": current_user.username,
                                       "student": equipment_application.student.username,
                                       "created_at": m.created_at
                                       }, messages))

        if form.validate_on_submit():
            message = Message()
            message.message = form.message.data
            message.equipment_application = equipment_application
            message.from_student = False
            reply_url = url_for(RouteConstants.HasStoryStudentView.MSG_TO_DONOR,
                                equipment_application_id=equipment_application_id,
                                _external=True)
            message_email(equipment_application.student, equipment_application.donor, message.message, reply_url)
            flask.g.session.add(message)
            flask.g.session.commit()
            return redirect(
                url_for(RouteConstants.DonorView.MSG_TO_STUDENT, equipment_application_id=equipment_application_id))
        return render_template(TemplateConstants.MESSAGE, messages=messages, other=current_user.username,
                               user_type=current_user.user_type, other_role=_("Donor"),
                               student=equipment_application.student.username, form=form)

    def download_equipment_receipts(self, equipment_id: int):
        current_app.logger.info(equipment_id)
        equipment = flask.g.session.query(Equipment).join(EquipmentApplication).filter(
            and_(
                Equipment.donor == current_user,
                Equipment.status == EquipmentStatusEnum.completed,
                Equipment.id == equipment_id,
                EquipmentApplication.status == EquipmentApplicationStatusEnum.completed_with_receipt
            )).first()
        if equipment is None:
            return render_template(TemplateConstants.Errors.STATUS_404), 404

        buffer = io.BytesIO()
        my_doc = SimpleDocTemplate(buffer)
        flowable_contents = []

        sample_style_sheet = getSampleStyleSheet()

        flowable_contents.append(Paragraph("iShare.support Donation Receipts", sample_style_sheet['Heading1']))

        flowable_contents.append(Paragraph(
            "To: " + equipment.donor.first_name + " " + equipment.donor.last_name,
            sample_style_sheet['BodyText']
        ))
        flowable_contents.append(Paragraph(
            "Thank you for your donation - " + equipment.equipment_type.name,
            sample_style_sheet['BodyText']
        ))
        flowable_contents.append(Paragraph(
            "and the equipment has received by " + equipment.equipment_application.student.first_name + " "
            + equipment.equipment_application.student.last_name,
            sample_style_sheet['BodyText']
        ))
        flowable_contents.append(Paragraph(
            "at cost $HKD " + str(equipment.receipt_total),
            sample_style_sheet['BodyText']
        ))
        flowable_contents.append(Paragraph(
            "",
            sample_style_sheet['BodyText']
        ))
        flowable_contents.append(Paragraph(
            "Reference Number: " + str(equipment.id),
            sample_style_sheet['BodyText']
        ))
        my_doc.build(flowable_contents)

        buffer.seek(0)

        return send_file(buffer, as_attachment=True, attachment_filename='receipts.pdf', mimetype='application/pdf')
