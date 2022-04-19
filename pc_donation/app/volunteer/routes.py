import json

import flask
from flask import redirect, url_for, render_template, jsonify, request, flash
from flask_babel import _, get_locale
from flask_classful import route
from flask_login import current_user
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from app.common.base_flask_view import BaseFlaskView
from app.common.decorator import is_volunteer
from app.common.email import message_email
from app.common.form import get_msg_form
from app.model.models import RepairApplication, Student, Story, Message
from app.model.status_enum import RepairApplicationStatusEnum
from app.route_constants import RouteConstants
from app.template_constants import TemplateConstants
from app.volunteer.forms import AppointmentForm
from config import GoogleMapConfig, AiChatbotConfig
from app.static_function import PageSet


class VolunteerView(BaseFlaskView):
    decorators = [is_volunteer]

    @staticmethod
    def _populate_make_repair_application_form_to_model(form, repair_application):
        repair_application.time = form.date_time.data
        repair_application.status = RepairApplicationStatusEnum.repairing
        repair_application.volunteer = current_user

    def index(self):
        lang = str(get_locale())

        return render_template(TemplateConstants.Volunteer.INDEX, title=_("Volunteer View"),
                               lang=lang,
                               key=AiChatbotConfig.volunteer_chatbot_key)

    def volunteer_repair_item_case(self):
        return render_template(TemplateConstants.Volunteer.VOLUNTEER_CHOOSE_REPAIR_EQUIPMENT_CASE,
                               title=_("Volunteer Repair"),
                               key=GoogleMapConfig.KEY)

    def repair_case_json(self):
        bound = json.loads(request.args.get("bound"))
        additional_filter = json.loads(request.args.get("additionalFilter"))
        language = additional_filter["language"]
        applications = flask.g.session.query(RepairApplication).join(Student).join(Story).options(
            joinedload(RepairApplication.student).subqueryload(Student.story)).filter(
            and_(
                RepairApplication.latitude < bound["north"],
                RepairApplication.latitude > bound["south"],
                RepairApplication.longitude < bound["east"],
                RepairApplication.longitude > bound["west"],
                RepairApplication.status == RepairApplicationStatusEnum.pending
            )).order_by(
            Story.urgency.desc())

        applications = list(applications)
        number_of_case = len(applications)
        ranks = [sorted(applications, key=lambda a: a.student.story.urgency).index(x) + 1 for x in applications]
        max_rank = max(max(ranks), 1)
        data = [{"id": a.id,
                 "latitude": a.latitude,
                 "longitude": a.longitude,
                 "title": a.title,
                 "description": a.student.story.content_en if language == "en" else a.student.story.content_zh_Hant,
                 "created_at": a.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
                 "image": a.equipment_photo,
                 "url": url_for(RouteConstants.VolunteerView.CREATE_REPAIR_APPLICATION, application_id=a.id),
                 "urgency": a.student.story.urgency,
                 "opacity": max(0.1, ranks[i] / max_rank)} for i, a in enumerate(applications)]

        if number_of_case == 0:
            return {"status": "ok", "data": []}
        if number_of_case > 500:
            return {"status": _("More than 500 records found, and please zoom in!"), "data": []}
        return jsonify({"status": "ok", "data": data})

    @route("/create-repair-application/<application_id>", methods=["GET", "POST"])
    def create_repair_application(self, application_id: int):
        repair_application = flask.g.session.query(RepairApplication).filter_by(
            id=application_id).first()
        form = AppointmentForm(obj=repair_application)
        form.first_name.data = repair_application.student.first_name
        form.last_name.data = repair_application.student.last_name
        if repair_application.status is not RepairApplicationStatusEnum.pending:
            flash(_("Appointment has already made!"))
            return redirect(url_for(RouteConstants.VolunteerView.INDEX))
        if form.validate_on_submit():
            self._populate_make_repair_application_form_to_model(form, repair_application)

            message_to_student = Message()
            message_to_student.message = _("Hello, let me help you fix your equipment and my prefer time is ") \
                                         + repair_application.time.strftime("%Y-%m-%dT%H:%M:%SZ")
            message_to_student.repair_application = repair_application
            message_to_student.from_student = False

            reply_url = url_for(RouteConstants.HasStoryStudentView.MSG_TO_VOLUNTEER,
                                repair_application_id=repair_application.id,
                                _external=True)
            message_email(repair_application.student, repair_application.volunteer, message_to_student.message,
                          reply_url)

            message_to_volunteer = Message()
            message_to_volunteer.message = _("Thank you for helping me!")
            message_to_volunteer.repair_application = repair_application
            message_to_volunteer.from_student = True

            reply_url = url_for(RouteConstants.VolunteerView.MSG_TO_STUDENT,
                                repair_application_id=repair_application.id,
                                _external=True)
            message_email(repair_application.volunteer, repair_application.student, message_to_volunteer.message,
                          reply_url)

            flask.g.session.add(message_to_student)
            flask.g.session.add(message_to_volunteer)
            flask.g.session.commit()
            flash(_("Equipment Repair Appointment has made!"))
            return redirect(url_for(RouteConstants.VolunteerView.VOLUNTEER_RECORD))
        return render_template(TemplateConstants.Volunteer.REPAIR_APPLICATION,
                               title=_("Create Repair Application"),
                               form=form, repair_application=repair_application)

    @route("/edit-repair-application/<repair_application_id>", methods=["GET", "POST"])
    def edit_repair_application(self, repair_application_id: int):
        repair_application = flask.g.session.query(RepairApplication).filter_by(
            id=repair_application_id).filter_by(
            volunteer=current_user).first()
        form = AppointmentForm(obj=repair_application)
        form.first_name.data = repair_application.student.first_name
        form.last_name.data = repair_application.student.last_name
        if form.validate_on_submit():
            self._populate_make_repair_application_form_to_model(form, repair_application)
            flask.g.session.commit()
            flash(_("Updated"))
            message = Message()
            message.message = _("Hello, I want to change the repair time to ") \
                              + repair_application.time.strftime("%Y-%m-%dT%H:%M:%SZ")
            message.repair_application = repair_application
            message.from_student = False
            reply_url = url_for(RouteConstants.VolunteerView.MSG_TO_STUDENT,
                                repair_application_id=repair_application.id,
                                _external=True)
            message_email(repair_application.student, current_user, message.message,
                          reply_url)
            return redirect(url_for(RouteConstants.VolunteerView.VOLUNTEER_RECORD))
        return render_template(TemplateConstants.Volunteer.REPAIR_APPLICATION, title=_("Edit Repair Application"),
                               form=form, repair_application=repair_application)

    @route("/cancel-make-repair-application/<repair_application_id>", methods=["GET"])
    @is_volunteer
    def cancel_make_repair_application(self, repair_application_id: int):
        repair_application = flask.g.session.query(RepairApplication).filter_by(id=repair_application_id) \
            .filter_by(volunteer=current_user) \
            .filter_by(status=RepairApplicationStatusEnum.repairing) \
            .first()
        if repair_application is None:
            return render_template(TemplateConstants.Errors.STATUS_404), 404
        repair_application.time = None
        repair_application.status = RepairApplicationStatusEnum.pending
        repair_application.volunteer = None

        message = Message()
        message.message = _("Sorry, I need to cancel your support case!")
        message.repair_application = repair_application
        message.from_student = False
        reply_url = url_for(RouteConstants.VolunteerView.MSG_TO_STUDENT, repair_application_id=repair_application.id,
                            _external=True)
        message_email(repair_application.student, current_user, message.message,
                      reply_url)
        flask.g.session.add(message)
        flask.g.session.commit()
        pass
        flask.g.session.commit()
        return redirect(url_for(RouteConstants.VolunteerView.VOLUNTEER_RECORD))

    def volunteer_record(self):
        '''repair_record = flask.g.session.query(RepairApplication).filter_by(
            volunteer_id=current_user.id).all()'''
        page = request.args.get('page', default=1, type=int)
        last_item = flask.g.session.query(RepairApplication).filter_by(
            volunteer_id=current_user.id).count()
        paging = PageSet(page, 4, last_item)
        repair_record = flask.g.session.query(RepairApplication).filter_by(
            volunteer_id=current_user.id).slice(paging.item_start, paging.item_end)
        return render_template(TemplateConstants.Volunteer.VOLUNTEER_RECORD, title=_("Volunteer Record"),
                               repair_record=repair_record, RepairApplicationStatusEnum=RepairApplicationStatusEnum, page=page, last_page=paging.last_page, page_list=paging.page_list)

    @route("/msg-to-student/<repair_application_id>", methods=["GET", "POST"])
    def msg_to_student(self, repair_application_id: int):
        repair_application = flask.g.session.query(RepairApplication).join(Message).join(Student).filter(
            and_(
                RepairApplication.id == repair_application_id,
                RepairApplication.status == RepairApplicationStatusEnum.repairing
            )).first()
        if repair_application is None or repair_application.messages is None:
            return redirect(url_for(RouteConstants.VolunteerView.VOLUNTEER_RECORD))

        messages = repair_application.messages.order_by(Message.created_at.desc())
        form = get_msg_form(messages)
        messages = list(map(lambda m: {"from_student": m.from_student, "message": m.message,
                                       "other": current_user.username,
                                       "student": repair_application.student.username,
                                       "created_at": m.created_at
                                       }, messages))
        repair_application = flask.g.session.query(RepairApplication).filter_by(
            volunteer=current_user,
            id=repair_application_id).first()

        if form.validate_on_submit():
            message = Message()
            message.message = form.message.data
            message.repair_application = repair_application
            message.from_student = False
            reply_url = url_for(RouteConstants.HasStoryStudentView.MSG_TO_VOLUNTEER,
                                repair_application_id=repair_application.id,
                                _external=True)
            message_email(repair_application.student, repair_application.volunteer, message.message,
                          reply_url)
            flask.g.session.add(message)
            flask.g.session.commit()
            return redirect(repair_application_id)
        return render_template(TemplateConstants.MESSAGE, messages=messages,
                               student=repair_application.student.username,
                               user_type=current_user.user_type,
                               other_role=_("Student"), form=form, other=current_user.username)
