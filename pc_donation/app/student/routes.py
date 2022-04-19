import flask
from flask import current_app
from flask import redirect, url_for, flash, render_template, request
from flask_babel import _, get_locale
from flask_classful import route
from flask_login import current_user
from sqlalchemy import and_

from app.common.base_flask_view import BaseFlaskView
from app.common.decorator import is_student, has_story
from app.common.email import message_email, ask_teacher_endorse_equipment_application_email, \
    thank_you_message_email_to_donor, \
    thank_you_message_email_to_volunteer
from app.common.form import get_msg_form
from app.common.form_helper import populate_form_equipment_types
from app.common.model_query import query_application_by_id
from app.model.models import EquipmentType, RepairApplication, EquipmentApplication, Story, \
    Message, Volunteer
from app.model.status_enum import EquipmentStatusEnum, EquipmentApplicationStatusEnum, RepairApplicationStatusEnum
from app.route_constants import RouteConstants
from app.student.forms import RepairApplicationForm, StudentStoryForm, \
    EquipmentApplicationForm, ThankToVolunteerForm, ViewStudentStoryForm, ThankToDonorForm, \
    EquipmentApplicationLocationForm
from app.template_constants import TemplateConstants
from config import GoogleMapConfig, AiChatbotConfig, Config
from app.static_function import PageSet


class StudentView(BaseFlaskView):
    decorators = [is_student]
    default_methods = ["GET", "POST"]

    @staticmethod
    def _populate_story_form_to_model(form, story):
        story.student = current_user
        form.populate_obj(story)

    def index(self):
        
        lang = str(get_locale())

        return render_template(TemplateConstants.Student.INDEX, title=_("Student View"),
                               lang=lang, key=AiChatbotConfig.student_chatbot_key)

    # TODO re-do 180 limit day to apply equipment
    def story(self):
        if current_user.story:
            form = ViewStudentStoryForm(obj=current_user.story)
            return render_template(TemplateConstants.Student.STORY, title=_("Story"), form=form,
                                   story_id=current_user.story.id, story=current_user.story)
        else:
            form = StudentStoryForm()
            if form.validate_on_submit():
                story_in_model = Story()
                self._populate_story_form_to_model(form, story_in_model)
                story_in_model.id = None
                flask.g.session.add(story_in_model)
                flask.g.session.commit()
                flash(_("Your story has submitted!"))
                return redirect(url_for(RouteConstants.StudentView.STORY))
            return render_template(TemplateConstants.Student.STORY, title=_("Story"), form=form)
            # return redirect(url_for(RouteConstants.Student.EDIT_STORY, story_id=has_story.id))
            # applicationCount = flask.g.session.query(Application).filter_by(user=current_user).count()
            # if applicationCount == 0:
            #     return redirect(url_for("student.application_story"))
            # elif applicationCount != 0:
            #     applicationTime = flask.g.session.query(Application).filter_by(user=current_user).order_by(
            #         Application.id.desc()).first()
            #     timeCheck = datetime.now() - datetime.strptime(applicationTime.idtime, "%Y-%m-%d %H:%M:%S")
            #     if applicationTime.apply_status_id == 6:
            #         if timeCheck.days < 30:
            #             flash(_("Each time the application was rejected, Need after 30 days apart to be able to re-apply"))
            #             return redirect(url_for("student.student_view"))
            #     elif timeCheck.days < 180:
            #         flash(_("Each application needs to be at least 180 days apart"))
            #         return redirect(url_for("student.student_view"))
            # if request.method == "POST":
            #     old_story = flask.g.session(Application).filter_by(user_id=current_user.id).order_by(
            #         Application.id.desc()).first()
            #     applications = Application(title=old_story.title, story=old_story.story,
            #                                user=current_user, apply_status_id=8,
            #                                apply_photo=old_story.apply_photo,
            #                                idtime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def edit_story(self, story_id: int):
        current_story_in_model = flask.g.session.query(Story).filter_by(id=story_id).filter_by(
            student=current_user).first()
        form = StudentStoryForm(obj=current_story_in_model)
        if form.validate_on_submit():
            self._populate_story_form_to_model(form, current_story_in_model)
            flask.g.session.add(current_story_in_model)
            flask.g.session.commit()
            return redirect(url_for(RouteConstants.StudentView.INDEX))
        return render_template(TemplateConstants.Student.STORY, title=_("Edit Story"), form=form, story_id=story_id,
                               story=current_story_in_model)


class HasStoryStudentView(BaseFlaskView):
    decorators = [is_student, has_story]
    default_methods = ["GET", "POST"]

    @staticmethod
    def _populate_repair_application_form_to_model(form, application):
        application.student = current_user
        form.populate_obj(application)
        application.status = RepairApplicationStatusEnum.pending

    @staticmethod
    def _populate_form_equipment_application(form, equipment_type_list):
        chosen_equipment_type_list = list(map(lambda x: x.equipment_type_id, equipment_type_list))
        # TODO: delete old method
        # form.equipment_type.choices = [(equipment_type.id, _(equipment_type.name)) for equipment_type in
        #                                flask.g.session.query(EquipmentType).filter(
        #                                    ~EquipmentType.id.in_(chosen_equipment_type_list)).all()]
        # example to remove for loop
        equipment_type_list = flask.g.session.query(EquipmentType).filter(
            ~EquipmentType.id.in_(chosen_equipment_type_list)).all()
        form.equipment_type_id.choices = list(map(lambda x: (x.id, x.name), equipment_type_list))
        # TODO: think how to use it later
        # equipment_type_list = flask.g.session.query(EquipmentType.id, EquipmentType.name).filter(
        #     ~EquipmentType.id.in_(chosen_equipment_type_list)).all()
        # form.equipment_type.choices = equipment_type_list

    def create_equipment_application(self):
        equipment_application_list = flask.g.session.query(EquipmentApplication).filter_by(
            student=current_user).filter_by(status=EquipmentApplicationStatusEnum.waiting_for_teacher_approval).all()
        form = EquipmentApplicationForm()
        if equipment_application_list:
            self._populate_form_equipment_application(form, equipment_application_list)
        else:
            populate_form_equipment_types(form)
        if form.validate_on_submit():
            # TODO: Logic to block too frequent application
            equipment_application = EquipmentApplication(
                status=EquipmentApplicationStatusEnum.waiting_for_teacher_approval,
                student=current_user,
                latitude=current_user.latitude,
                longitude=current_user.longitude,
                equipment_type_id=form.equipment_type_id.data)

            flask.g.session.add(equipment_application)
            flask.g.session.commit()
            flash(_("Your request add successfully"))
            return redirect(url_for(RouteConstants.HasStoryStudentView.CREATE_EQUIPMENT_APPLICATION))
        return render_template(TemplateConstants.Student.CREATE_EQUIPMENT_APPLICATION, title=_("Equipment Application"),
                               form=form, equipment_application_list=equipment_application_list)

    @route("/cancel-requested_equipment-application/<equipment_application_id>", methods=["GET"])
    def cancel_requested_equipment_application(self, equipment_application_id: int):
        requested_equipment = flask.g.session.query(EquipmentApplication).filter_by(student=current_user).filter_by(
            id=equipment_application_id).filter_by(
            status=EquipmentApplicationStatusEnum.waiting_for_teacher_approval).first()
        if requested_equipment is None:
            return render_template(TemplateConstants.Errors.STATUS_404), 404
        flask.g.session.delete(requested_equipment)
        flask.g.session.commit()
        return redirect(url_for(RouteConstants.HasStoryStudentView.CREATE_EQUIPMENT_APPLICATION))

    def equipment_application_map(self):
        form = EquipmentApplicationLocationForm()
        if form.validate_on_submit():
            equipment_applications = flask.g.session.query(EquipmentApplication).filter_by(
                student=current_user).filter_by(
                status=EquipmentApplicationStatusEnum.waiting_for_teacher_approval).all()

            for equipment_application in equipment_applications:
                equipment_application.latitude = form.latitude.data
                equipment_application.longitude = form.longitude.data

            ask_teacher_endorse_equipment_application_email(current_user)
            flask.g.session.commit()
            return redirect(url_for(RouteConstants.HasStoryStudentView.EQUIPMENT_APPLICATION_HISTORY))
        return render_template(TemplateConstants.Student.EQUIPMENT_APPLICATION_MAP,
                               title=_("Equipment Application Map"),
                               form=form,
                               key=GoogleMapConfig.KEY)

    @route("/equipment-application-history", methods=["GET"])
    def equipment_application_history(self):
        '''equipment_applications = flask.g.session.query(EquipmentApplication).filter_by(
            student=current_user).order_by(
            EquipmentApplication.created_at.desc()).all()'''
        page = request.args.get('page', default=1, type=int)
        last_item = flask.g.session.query(EquipmentApplication).filter_by(student=current_user).count()
        paging = PageSet(page, Config.PAGING_PER_PAGE, last_item)
        equipment_applications = flask.g.session.query(EquipmentApplication).filter_by(
            student=current_user).order_by(EquipmentApplication.created_at.desc()).slice(paging.item_start, paging.item_end)
        return render_template(TemplateConstants.Student.EQUIPMENT_APPLICATION_HISTORY, title=_("Application History"),
                               equipment_applications=equipment_applications,
                               EquipmentApplicationStatusEnum=EquipmentApplicationStatusEnum, page=page, last_page=paging.last_page, page_list=paging.page_list)

    # complete before thank you
    @route("/complete-equipment-application/<equipment_application_id>", methods=["GET"])
    def complete_equipment_application(self, equipment_application_id: int):
        equipment_application = query_application_by_id(application_model=EquipmentApplication,
                                                        application_id=equipment_application_id)
        current_app.logger.info(equipment_application)

        if equipment_application.status == EquipmentApplicationStatusEnum.in_progress:
            flash(
                _("Write a thank you letter to your donor, else you cannot apply any new equipment or support!"))
            equipment_application.status = EquipmentApplicationStatusEnum.donated
            equipment_application.equipment.status = EquipmentStatusEnum.completed
            flask.g.session.commit()
        return redirect(url_for(RouteConstants.HasStoryStudentView.THANKS_TO_DONOR_COMPLETE_EQUIPMENT_APPLICATION,
                                equipment_application_id=equipment_application_id))

    def new_repair_application(self):
        form = RepairApplicationForm()
        if form.validate_on_submit():
            repair_application = RepairApplication()
            repair_application.student = current_user
            self._populate_repair_application_form_to_model(form, repair_application)
            repair_application.id = None

            flask.g.session.add(repair_application)
            flask.g.session.commit()
            flash(_("Your repair application has submitted!"))
            return redirect(url_for(RouteConstants.StudentView.INDEX))
        return render_template(TemplateConstants.Student.EDIT_REPAIR_APPLICATION, title=_("New Repair Application"),
                               form=form,
                               action=url_for(RouteConstants.HasStoryStudentView.NEW_REPAIR_APPLICATION),
                               youtube="Repair")

    def edit_repair_application(self, repair_application_id: int):
        current_repair_application = flask.g.session.query(RepairApplication).filter_by(
            id=repair_application_id).filter_by(
            student=current_user).first()
        current_app.logger.info(current_repair_application)
        form = RepairApplicationForm(obj=current_repair_application)
        current_app.logger.info(form)
        if form.validate_on_submit():
            self._populate_repair_application_form_to_model(form, current_repair_application)
            flask.g.session.commit()
            flash(_("Updated"))
            return redirect(url_for(RouteConstants.HasStoryStudentView.REPAIR_APPLICATION_LIST))
        return render_template(TemplateConstants.Student.EDIT_REPAIR_APPLICATION,
                               title=_("Edit Repair Application"),
                               form=form,
                               action=url_for(RouteConstants.HasStoryStudentView.EDIT_REPAIR_APPLICATION,
                                              repair_application_id=repair_application_id),
                               key=GoogleMapConfig.KEY)

    @route("/repair-history-list", methods=["GET"])
    def repair_application_list(self):
        '''repair_applications = flask.g.session.query(RepairApplication).filter_by(
            student=current_user).all()'''
        page = request.args.get('page', default=1, type=int)
        last_item = flask.g.session.query(RepairApplication).filter_by(student=current_user).count()
        paging = PageSet(page, Config.PAGING_PER_PAGE, last_item)
        repair_applications = flask.g.session.query(RepairApplication).filter_by(student=current_user).slice(paging.item_start,paging.item_end)
        return render_template(TemplateConstants.Student.REPAIR_APPLICATION_LIST, title=_("Repair History"),
                               applications=repair_applications,
                               RepairApplicationStatusEnum=RepairApplicationStatusEnum, page=page, last_page=paging.last_page, page_list=paging.page_list)

    def repair_application(self, repair_application_id: int):
        repair_application = flask.g.session.query(RepairApplication).filter_by(
            id=repair_application_id).filter_by(
            student=current_user).first()
        current_app.logger.info(repair_application)
        if repair_application is None:
            return render_template(TemplateConstants.Errors.STATUS_404), 404

        return render_template(TemplateConstants.Student.REPAIR_APPLICATION, title=_("Application History"),
                               repair_application=repair_application,
                               RepairApplicationStatusEnum=RepairApplicationStatusEnum)

    @route("/delete-repair-application/<repair_application_id>", methods=["GET"])
    def delete_repair_application(self, repair_application_id: int):
        repair = flask.g.session.query(RepairApplication).filter_by(id=repair_application_id) \
            .filter_by(student=current_user) \
            .filter_by(status=RepairApplicationStatusEnum.pending) \
            .first()
        current_app.logger.info(repair)
        if repair is None:
            return render_template(TemplateConstants.Errors.STATUS_404), 404
        flask.g.session.delete(repair)
        flask.g.session.commit()
        return redirect(url_for(RouteConstants.HasStoryStudentView.REPAIR_APPLICATION_LIST))

    @route("/student-complete-repair-equipment/<repair_application_id>", methods=["GET"])
    def student_complete_repair_equipment(self, repair_application_id: int):
        repair_application = query_application_by_id(application_model=RepairApplication,
                                                     application_id=repair_application_id)

        if repair_application.status == RepairApplicationStatusEnum.repairing:
            flash(
                _("Write a thank you letter to your volunteer, else you cannot apply any new equipment or support!"))
            repair_application.status = RepairApplicationStatusEnum.repaired
            flask.g.session.commit()

        return redirect(url_for(RouteConstants.HasStoryStudentView.THANKS_TO_VOLUNTEER_COMPLETE_REPAIR_EQUIPMENT,
                                repair_application_id=repair_application_id))

    def msg_to_donor(self, equipment_application_id: int):
        equipment_application = flask.g.session.query(EquipmentApplication).filter_by(student=current_user).filter_by(
            id=equipment_application_id).filter_by(
            status=EquipmentApplicationStatusEnum.in_progress).first()
        if equipment_application is None or equipment_application.messages is None:
            return redirect(url_for(RouteConstants.HasStoryStudentView.EQUIPMENT_APPLICATION_HISTORY))

        messages = equipment_application.messages.order_by(Message.created_at.desc())
        form = get_msg_form(messages)
        messages = list(map(lambda m: {"from_student": m.from_student, "message": m.message,
                                       "other": current_user.username,
                                       "volunteer": equipment_application.donor.username,
                                       "created_at": m.created_at
                                       }, messages))

        if form.validate_on_submit():
            message_donor = Message()
            message_donor.message = form.message.data
            message_donor.equipment_application = equipment_application
            message_donor.from_student = True

            reply_url = url_for(RouteConstants.DonorView.MSG_TO_STUDENT,
                                equipment_application_id=equipment_application_id,
                                _external=True)
            message_email(equipment_application.donor, equipment_application.student, message_donor.message,
                          reply_url)

            flask.g.session.add(message_donor)
            flask.g.session.commit()
            return redirect(
                url_for(RouteConstants.HasStoryStudentView.MSG_TO_DONOR,
                        equipment_application_id=equipment_application_id))
        return render_template(TemplateConstants.MESSAGE, messages=messages, other=current_user,
                               user_type=current_user.user_type,
                               volunteer=equipment_application.donor.username,
                               other_role=_("Donor"), form=form)

    def msg_to_volunteer(self, repair_application_id: int):
        repair_application = flask.g.session.query(RepairApplication).join(Volunteer).filter(
            and_(
                RepairApplication.student == current_user,
                RepairApplication.id == repair_application_id,
                RepairApplication.status == RepairApplicationStatusEnum.repairing
            )).first()
        if repair_application is None or repair_application.messages is None:
            return redirect(url_for(RouteConstants.HasStoryStudentView.REPAIR_APPLICATION_LIST))
        messages = repair_application.messages.order_by(Message.created_at.desc())
        form = get_msg_form(messages)
        messages = list(map(lambda m: {"from_student": m.from_student, "message": m.message,
                                       "other": current_user.username,
                                       "volunteer": repair_application.volunteer.username,
                                       "created_at": m.created_at
                                       }, messages))
        repair_application = flask.g.session.query(RepairApplication).filter_by(
            student=current_user,
            id=repair_application_id).first()

        # current_app.logger.info(repair_application)
        if form.validate_on_submit():
            message_volunteer = Message()
            message_volunteer.message = form.message.data
            message_volunteer.repair_application = repair_application
            message_volunteer.from_student = True
            current_app.logger.info(repair_application.volunteer.username)

            reply_url = url_for(RouteConstants.VolunteerView.MSG_TO_STUDENT,
                                repair_application_id=repair_application_id,
                                _external=True)
            message_email(repair_application.volunteer, repair_application.student, message_volunteer.message,
                          reply_url)

            flask.g.session.add(message_volunteer)
            flask.g.session.commit()
            return redirect(
                url_for(RouteConstants.HasStoryStudentView.MSG_TO_VOLUNTEER,
                        repair_application_id=repair_application_id))
        return render_template(TemplateConstants.MESSAGE, messages=messages, other=current_user,
                               user_type=current_user.user_type,
                               volunteer=repair_application.volunteer.username,
                               other_role=_("Volunteer"), form=form)

    def thanks_to_donor_complete_equipment_application(self, equipment_application_id: int):
        equipment_application = query_application_by_id(application_model=EquipmentApplication,
                                                        application_id=equipment_application_id)
        if equipment_application.status == EquipmentApplicationStatusEnum.donated:
            form = ThankToDonorForm()
            if form.validate_on_submit():
                form.populate_obj(equipment_application)
                if equipment_application.equipment.has_receipt:
                    equipment_application.status = EquipmentApplicationStatusEnum.donated_waiting_for_receipt
                else:
                    equipment_application.status = EquipmentApplicationStatusEnum.completed_without_receipt
                thank_you_message_email_to_donor(to_user=equipment_application.donor,
                                                 from_user=equipment_application.student,
                                                 message=equipment_application.thanks_message)
                flask.g.session.commit()
                flash(_("Emailed the thanks message to your donor."))
                return redirect(url_for(RouteConstants.StudentView.INDEX))
            return render_template(TemplateConstants.Student.THANK_YOU,
                                   title=_("Thank Letter to your donor"), form=form,
                                   repair_application_id=equipment_application_id)
        else:
            return redirect(url_for(RouteConstants.StudentView.INDEX))

    def thanks_to_volunteer_complete_repair_equipment(self, repair_application_id: int):
        repair_application = query_application_by_id(application_model=RepairApplication,
                                                     application_id=repair_application_id)
        if repair_application.status == RepairApplicationStatusEnum.repaired:
            form = ThankToVolunteerForm()
            if form.validate_on_submit():
                form.populate_obj(repair_application)
                repair_application.status = RepairApplicationStatusEnum.completed
                thank_you_message_email_to_volunteer(to_user=repair_application.volunteer,
                                                     from_user=repair_application.student,
                                                     message=repair_application.thanks_message)
                flask.g.session.commit()
                flash(_("send the thanks email to volunteer"))
                return redirect(url_for(RouteConstants.StudentView.INDEX))
            return render_template(TemplateConstants.Student.THANK_YOU,
                                   title=_("Student Thanks Volunteer to complete repair case "), form=form,
                                   repair_application_id=repair_application_id)
        else:
            return redirect(url_for(RouteConstants.StudentView.INDEX))
