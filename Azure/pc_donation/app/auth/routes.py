import json
from datetime import datetime

import flask
import tldextract
from flask import current_app
from flask import redirect, url_for, flash, request, render_template, session, jsonify
from flask_babel import _
from flask_classful import route
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import and_
from sqlalchemy.orm import with_polymorphic

from app import db
from app.auth.forms import LoginForm, ResetPasswordRequestForm, ResetPasswordForm, \
    TeacherForm, StudentForm, DonorForm, StudentSecondPageForm, \
    VolunteerForm, TeacherSecondPageForm, VolunteerSecondPageForm, ResentConfirmationEmailForm
from app.common.base_flask_view import BaseFlaskView
from app.common.decorator import logout_first
from app.common.email import token_to_email, password_reset_email, \
    confirmation_email_address_email, approved_other_account_email, \
    ask_teacher_create_account_then_approve_student_account_email, account_activated_email
from app.common.form_helper import populate_form_regions
from app.model.models import User, Student, Volunteer, Teacher, School, Donor, Admin
from app.model.status_enum import StudentStatusEnum, TeacherStatusEnum, SchoolCategoryEnum
from app.route_constants import RouteConstants
from app.template_constants import TemplateConstants


class AuthView(BaseFlaskView):
    route_base = "auth"

    @route("/resend-confirmation-email", methods=["GET", "POST"])
    @login_required
    def resend_confirmation_email(self):
        if current_user.activated:
            return redirect(url_for(RouteConstants.MainView.INDEX))
        form = ResentConfirmationEmailForm()
        if form.validate_on_submit():
            confirmation_email_address_email(current_user)
            flash(_("Your email confirmation email resend already."))
        return render_template(TemplateConstants.Auth.RESEND_CONFIRMATION_EMAIL, form=form)

    def logout(self):
        logout_user()
        if session.get("pre_login_url", ""):
            session.pop("pre_login_url")
        return redirect(url_for(RouteConstants.MainView.INDEX))

    def school_json(self):
        bound = json.loads(request.args.get("bound"))
        current_app.logger.info(bound)
        additional_filter = json.loads(request.args.get("additionalFilter"))
        current_app.logger.info(additional_filter)
        schools = flask.g.session.query(School).filter(
            and_(
                School.latitude < bound["north"],
                School.latitude > bound["south"],
                School.longitude < bound["east"],
                School.longitude > bound["west"],
                School.category == SchoolCategoryEnum(int(additional_filter["schoolCategory"]))
            ))

        schools = list(schools)
        number_of_school = len(schools)
        current_app.logger.info(number_of_school)
        data = [{"id": a.id,
                 "latitude": a.latitude,
                 "longitude": a.longitude,
                 "title": a.name_zh_Hant + " / " + a.name_en,
                 "description": str(a.category),
                 "domain": tldextract.extract(a.url).registered_domain
                 } for i, a in enumerate(schools)]

        if number_of_school == 0:
            return {"status": "ok", "data": []}
        if number_of_school > 500:
            return {"status": _("More than 500 records found, and please zoom in!"), "data": []}
        return jsonify({"status": "ok", "data": data})


class NoAuthView(BaseFlaskView):
    route_base = "auth"
    decorators = [logout_first]
    default_methods = ["GET", "POST"]

    @staticmethod
    def _student_update_own_status(student):
        if student.status == TeacherStatusEnum.activated:
            flash(_("You account has already activated."))
        elif student.status == StudentStatusEnum.not_activated or \
                student.status == StudentStatusEnum.student_activated_wait_for_teacher_approval:
            flash(_("student_activated_wait_for_teacher_approval"))
            student.status = StudentStatusEnum.student_activated_wait_for_teacher_approval
        elif student.status == StudentStatusEnum.student_not_activated_and_teacher_approved:
            student.status = StudentStatusEnum.activated
            account_activated_email(student)
            flash(_("You account has already activated."))

    @staticmethod
    def _teacher_update_own_status(teacher):
        if teacher.status == TeacherStatusEnum.activated:
            flash(_("You account has already activated."))
        elif teacher.status == TeacherStatusEnum.not_activated or \
                teacher.status == TeacherStatusEnum.teacher_activated_wait_for_admin_approval:
            flash(_("teacher_activated_wait_for_admin_approval"))
            teacher.status = TeacherStatusEnum.teacher_activated_wait_for_admin_approval
            current_app.logger.info(teacher.status)
        elif teacher.status == TeacherStatusEnum.teacher_not_activated_and_admin_approved:
            teacher.status = TeacherStatusEnum.activated
            account_activated_email(teacher)
            flash(_("You account has already activated."))

    def login(self):
        if current_user.is_authenticated:
            return redirect(url_for(RouteConstants.MainView.INDEX))
        form = LoginForm()
        if form.validate_on_submit():
            all_user_type = with_polymorphic(User, "*")
            user = flask.g.session.query(all_user_type).filter(
                db.or_(User.username == form.username.data, User.email == form.username.data)).first()
            if user is None or not user.check_password(form.password.data):
                flash(_("Invalid username or password"))
                return redirect(url_for(RouteConstants.NoAuthView.LOGIN))

            login_user(user, remember=form.remember_me.data)
            if not user.activated:
                if isinstance(user, Teacher) or isinstance(user, Student):
                    flash(_(user.status.name))
                redirect(RouteConstants.AuthView.RESEND_CONFIRMATION_EMAIL)
            next_page = session.get("pre_login_url", None)
            if next_page is None:
                if isinstance(user, Teacher):
                    next_page = url_for(RouteConstants.TeacherView.INDEX)
                elif isinstance(user, Volunteer):
                    next_page = url_for(RouteConstants.VolunteerView.INDEX)
                elif isinstance(user, Student):
                    next_page = url_for(RouteConstants.StudentView.INDEX)
                elif isinstance(user, Donor):
                    next_page = url_for(RouteConstants.DonorView.INDEX)
                elif isinstance(user, Admin):
                    next_page = url_for(RouteConstants.AdminView.INDEX)
            else:
                session.pop("pre_login_url")
            if current_user.is_authenticated:
                current_user.last_seen = datetime.utcnow()
                flask.g.session.commit()

            return redirect(next_page)
        return render_template(TemplateConstants.Auth.LOGIN, title=_("Sign In"), form=form)

    def confirm_email(self, token):
        email = token_to_email(token)
        if email:
            all_user_type = with_polymorphic(User, "*")
            user = flask.g.session.query(all_user_type).filter(User.email == email).first()
            current_app.logger.info(user)
            if user is None:
                flash(_("The confirmation link is invalid or has expired."), "danger")
                return redirect(url_for(RouteConstants.NoAuthView.LOGIN))
            if isinstance(user, Student):
                self._student_update_own_status(user)
            elif isinstance(user, Teacher):
                self._teacher_update_own_status(user)
            else:
                if user.activated:
                    flash(_("Account already confirmed. Please login."), "success")
                else:
                    user.activated = True
                    account_activated_email(user)
                    flash(_("You have confirmed your account. Thanks!"))
        else:
            flash(_("The confirmation link is invalid or has expired."), "danger")
        flask.g.session.commit()
        return redirect(url_for(RouteConstants.NoAuthView.LOGIN))

    def reset_password(self, token):
        user = User.verify_reset_password_token(token)
        if not user:
            flash(_("Invalid token and please reset again."))
            return redirect(url_for(RouteConstants.MainView.INDEX))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            user.set_password(form.password.data)
            flask.g.session.commit()
            flash(_("Your password has been reset."))
            return redirect(url_for(RouteConstants.NoAuthView.LOGIN))
        return render_template(TemplateConstants.Auth.RESET_PASSWORD, form=form)

    def reset_password_request(self):
        form = ResetPasswordRequestForm()
        if form.validate_on_submit():
            user = flask.g.session.query(User).filter_by(email=form.email.data).first()
            if user:
                password_reset_email(user)
            flash(
                _("Check your email for the instructions to reset your password"))
            return redirect(url_for(RouteConstants.NoAuthView.LOGIN))
        return render_template(TemplateConstants.Auth.RESET_PASSWORD_REQUEST,
                               title=_("Reset Password"),
                               form=form)

    def register_donor(self):
        form = DonorForm()
        populate_form_regions(form)
        if form.validate_on_submit():
            donor = Donor()
            form.populate_obj(donor)
            donor.set_password(form.password.data)
            confirmation_email_address_email(donor)
            flash(_("You already successful to register!"))
            flask.g.session.add(donor)
            flask.g.session.commit()
            return redirect(url_for(RouteConstants.NoAuthView.LOGIN))
        return render_template(TemplateConstants.Auth.REGISTER_FIRST_PAGE,
                               title=_("Register Donor"),
                               form=form)

    def register_student(self):
        form = StudentForm()
        populate_form_regions(form)
        if form.validate_on_submit():
            student = Student()
            form.populate_obj(student)
            student.set_password(form.password.data)
            session["previous_student_page_data"] = student.object_as_dict()
            return redirect(url_for(RouteConstants.NoAuthView.REGISTER_STUDENT_SECOND_PAGE))
        return render_template(TemplateConstants.Auth.REGISTER_FIRST_PAGE,
                               title=_("Register Student"),
                               form=form)

    def register_student_second_page(self):
        form = StudentSecondPageForm()
        previous_student_page_data = session["previous_student_page_data"]
        if form.validate_on_submit():
            student = Student(**previous_student_page_data)
            form.populate_obj(student)
            student.status = StudentStatusEnum.not_activated
            teacher = flask.g.session.query(Teacher).filter(Teacher.email == student.teacher_email).first()
            if teacher:
                student.teacher = teacher
                approved_other_account_email(student)
            else:
                ask_teacher_create_account_then_approve_student_account_email(student)
            confirmation_email_address_email(student)
            flash(_("You already successful to register!"))
            flask.g.session.add(student)
            flask.g.session.commit()
            session.pop("previous_student_page_data")
            return redirect(url_for(RouteConstants.MainView.INDEX))
        return render_template(TemplateConstants.Auth.REGISTER_STUDENT_SECOND_PAGE,
                               title=_("Register Student Second Page"), form=form,
                               school_categories=SchoolCategoryEnum.get_value_to_name_dict(),
                               action=url_for(RouteConstants.NoAuthView.REGISTER_STUDENT_SECOND_PAGE))

    def register_volunteer(self):
        if current_user.is_authenticated:
            return redirect(url_for(RouteConstants.MainView.INDEX))
        form = VolunteerForm()
        populate_form_regions(form)
        if form.validate_on_submit():
            volunteer = Volunteer()
            form.populate_obj(volunteer)
            volunteer.set_password(form.password.data)
            session["previous_volunteer_page_data"] = volunteer.object_as_dict()
            return redirect(url_for(RouteConstants.NoAuthView.REGISTER_VOLUNTEER_SECOND_PAGE))
        return render_template(TemplateConstants.Auth.REGISTER_FIRST_PAGE,
                               title=_("Register Volunteer"),
                               form=form)

    def register_volunteer_second_page(self):
        form = VolunteerSecondPageForm()
        if form.validate_on_submit():
            previous_volunteer_page_data = session["previous_volunteer_page_data"]
            volunteer = Volunteer(**previous_volunteer_page_data)
            form.populate_obj(volunteer)
            confirmation_email_address_email(volunteer)
            flash(_("You already successful to register!"))
            flask.g.session.add(volunteer)
            flask.g.session.commit()
            session.pop("previous_volunteer_page_data")
            return redirect(url_for(RouteConstants.MainView.INDEX))
        return render_template(TemplateConstants.Auth.REGISTER_VOLUNTEER_SECOND_PAGE,
                               title=_("Register Volunteer Second Page"),
                               form=form,
                               action=url_for(RouteConstants.NoAuthView.REGISTER_VOLUNTEER_SECOND_PAGE))

    def register_teacher(self):
        form = TeacherForm()
        teacher_email = request.args.get("email")
        session["teacher_email"] = teacher_email
        populate_form_regions(form)
        if form.validate_on_submit():
            teacher = Teacher()
            form.populate_obj(teacher)
            teacher.set_password(form.password.data)
            session["previous_teacher_page_data"] = teacher.object_as_dict()
            return redirect(url_for(RouteConstants.NoAuthView.REGISTER_TEACHER_SECOND_PAGE))
        return render_template(TemplateConstants.Auth.REGISTER_FIRST_PAGE,
                               title=_("Register Teacher"),
                               form=form)

    def register_teacher_second_page(self):
        form = TeacherSecondPageForm()
        if session.get("teacher_email") is not None:
            form.email.data = session["teacher_email"]
        school_categories = SchoolCategoryEnum.get_value_to_name_dict()
        previous_teacher_page_data = session["previous_teacher_page_data"]
        current_app.logger.info(previous_teacher_page_data)
        if form.validate_on_submit():
            previous_teacher_page_data = session["previous_teacher_page_data"]
            teacher = Teacher(**previous_teacher_page_data)
            form.populate_obj(teacher)
            teacher.status = TeacherStatusEnum.not_activated
            confirmation_email_address_email(teacher)
            flash(_("Our admin will review your account application and approve your application as soon as possible."))
            approved_other_account_email(teacher)
            flask.g.session.add(teacher)
            flask.g.session.commit()
            session.pop("previous_teacher_page_data")
            session.pop("teacher_email")
            return redirect(url_for(RouteConstants.MainView.INDEX))
        return render_template(TemplateConstants.Auth.REGISTER_TEACHER_SECOND_PAGE,
                               title=_("Register Teacher Second Page"),
                               school_categories=school_categories,
                               form=form)