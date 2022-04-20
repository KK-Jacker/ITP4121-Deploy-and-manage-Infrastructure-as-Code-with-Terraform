from functools import wraps

from flask import render_template, redirect, url_for, session, request, flash
from flask_babel import _
from flask_login import current_user, logout_user

from app.model.status_enum import StudentStatusEnum
from app.route_constants import RouteConstants
from app.template_constants import TemplateConstants


def is_user_type(user_type, func, *args, **kwargs):
    if not current_user.is_authenticated:
        if not session.get("pre_login_url", ""):
            session["pre_login_url"] = request.url
        return redirect(url_for(RouteConstants.NoAuthView.LOGIN))
    elif current_user.user_type != user_type:
        return redirect(url_for(RouteConstants.AuthView.LOGOUT))
    elif current_user.user_type == user_type:
        if not current_user.activated:
            return redirect(url_for(RouteConstants.AuthView.RESEND_CONFIRMATION_EMAIL))
        return func(*args, **kwargs)
    else:
        return render_template(TemplateConstants.Errors.STATUS_404), 404


# admin route
def is_admin(func):
    @wraps(func)
    def view(*args, **kwargs):
        return is_user_type("admin", func, *args, **kwargs)

    return view


# auth route
def logout_first(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if current_user.is_authenticated:
            logout_user()
        return func(*args, **kwargs)

    return decorator


# donor route
def is_donor(func):
    @wraps(func)
    def view(*args, **kwargs):
        return is_user_type("donor", func, *args, **kwargs)

    return view


# student route
def is_student(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        return is_user_type("student", func, *args, **kwargs)

    return decorated_view


def is_student_in_status(status: StudentStatusEnum):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.status == status:
                return func(*args, **kwargs)
            else:
                return render_template(TemplateConstants.Errors.STATUS_404), 404

        return wrapper

    return decorator


def has_story(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if current_user.story is None:
            flash(_("Please share your story!"))
            return redirect(url_for(RouteConstants.StudentView.STORY))
        return func(*args, **kwargs)

    return decorator


# teacher route
def is_teacher(func):
    @wraps(func)
    def view(*args, **kwargs):
        return is_user_type("teacher", func, *args, **kwargs)

    return view


# volunteer route
def is_volunteer(func):
    @wraps(func)
    def volunteers_view(*args, **kwargs):
        return is_user_type("volunteer", func, *args, **kwargs)

    return volunteers_view


def is_activated(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_active:
            return redirect(url_for(RouteConstants.AuthView.RESEND_CONFIRMATION_EMAIL))
        return func(*args, **kwargs)

    return decorated_function
