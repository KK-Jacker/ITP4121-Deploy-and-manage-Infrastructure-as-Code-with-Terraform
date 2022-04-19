import flask
from flask import render_template, flash, redirect, url_for, request, session, current_app
from flask_babel import _
from flask_classful import route
from flask_login import current_user, login_required

from app import BaseFlaskView
from app import RouteConstants, TemplateConstants
from app.common.decorator import is_activated
from app.common.form_helper import populate_form_regions
from app.main.forms import EditProfileForm
from app.model.models import User
from config import AiChatbotConfig


# Other methods for route class
# class UserView(MainView, View):
#     methods = ["GET"]
#
#     def dispatch_request(self, username):
#         return "Hello %s!" % username
#
#
# bp.add_url_rule("/beta_user/<username>", view_func=UserView.as_view("beta_user_view"))


class MainView(BaseFlaskView):
    route_base = "/"

    def index(self):
        categories = [
            {
                "link_name": url_for(RouteConstants.NoAuthView.REGISTER_DONOR),
                "name": _("Donor"),
                "body": _("index_page_donate_info")
            },
            {
                "link_name": url_for(RouteConstants.NoAuthView.REGISTER_STUDENT),
                "name": _("Student"),
                "body": _("index_page_student_info")
            },
            {
                "link_name": url_for(RouteConstants.MainView.SUPPORTERS),
                "name": _("Volunteer"),
                "body": _("index_page_volunteer_info")
            }
        ]
        # isTeacher = None
        current_app.logger.info(current_user)
        if current_user.is_authenticated:
            if not current_user.activated:
                return redirect(url_for(RouteConstants.AuthView.RESEND_CONFIRMATION_EMAIL))
            elif current_user.user_type == "admin":
                return redirect(url_for(RouteConstants.AdminView.INDEX))
            elif current_user.user_type == "donor":
                return redirect(url_for(RouteConstants.DonorView.INDEX))
            elif current_user.user_type == "student":
                return redirect(url_for(RouteConstants.StudentView.INDEX))
            elif current_user.user_type == "teacher":
                return redirect(url_for(RouteConstants.TeacherView.INDEX))
            elif current_user.user_type == "volunteer":
                return redirect(url_for(RouteConstants.VolunteerView.INDEX))
            return render_template(TemplateConstants.INDEX,
                                   title=_("Home"),
                                   categories=categories,
                                   withoutcontainer=True,
                                   key=AiChatbotConfig.anonymous_chatbot_key)
        else:
            return render_template(TemplateConstants.INDEX,
                                   title=_("Home"),
                                   categories=categories,
                                   withoutcontainer=True,
                                   key=AiChatbotConfig.anonymous_chatbot_key)

    def supporters(self):
        supporters = [
            {
                "link_name": url_for(RouteConstants.NoAuthView.REGISTER_TEACHER),
                "name": _("Teacher"),
                "body": _("volunteer_page_teacher_info")
            },
            {
                "link_name": url_for(RouteConstants.NoAuthView.REGISTER_VOLUNTEER),
                "name": _("Volunteer"),
                "body": _("volunteer_page_volunteer_info")
            }

        ]
        return render_template(TemplateConstants.SUPPORTERS,
                               title=_("Supporters"),
                               supportors=supporters)

    @login_required
    @is_activated
    def user(self, username):
        login_user = flask.g.session.query(User).filter_by(username=username).first()
        return render_template(TemplateConstants.USER,
                               title=_("User"),
                               user=login_user)

    @route("/edit-profile", methods=["GET", "POST"])
    @login_required
    @is_activated
    def edit_profile(self):
        form = EditProfileForm(obj=current_user, original_username=current_user.username)
        populate_form_regions(form)
        current_app.logger.info(current_user.region)
        if form.validate_on_submit():
            current_user_data = current_user
            form.populate_obj(current_user_data)
            flask.g.session.add(current_user_data)
            flask.g.session.commit()
            flash(_("Your changes have been saved."))
            return redirect(url_for(RouteConstants.MainView.USER, username=current_user.username))

        return render_template(TemplateConstants.EDIT_PROFILE,
                               title=_("Edit Profile"),
                               form=form,
                               username=current_user.username)

    def language(self, language="zh"):

        language = request.args.get('language')

        if language == "zh":
            language = "zh_Hant"
        session["language"] = language
        return redirect(request.referrer)

    def terms(self):
        return render_template(TemplateConstants.TERMS, title=_("Terms"))

    def about_us(self):
        return render_template(TemplateConstants.ABOUT_US, title=_("About US"))
