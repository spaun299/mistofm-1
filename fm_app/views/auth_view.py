from ..blueprints import auth_blueprint
from flask import redirect, url_for
from flask_login import logout_user, login_required
# from ..models import User
# from flask_user.views import _call_or_get, signals
# from flask_user.passwords import verify_password
#
#
# @auth_blueprint.route('/login', methods=['POST'])
# def login():
#     """ Prompt for username/email and password and sign the user in."""
#     user_manager = current_app.user_manager
#     data = request.form
#     next = request.args.get('next', '/')
#     if _call_or_get(current_user.is_authenticated) and user_manager.auto_login_at_login:
#         return redirect(next)
#     user = g.db.query(User).filter_by(username=data.get('user_name')).first()
#     if not user:
#         flash("Incorrect name or password")
#     else:
#         if user.password:
#             if not verify_password(user_manager, data.get('password'), user.password):
#                 flash("Incorrect name or password")
#         else:
#             flash("Incorrect name or password")
#     remember_me = True if data.get('remember_me') else False
#     if user:
#         login_user(user, remember=remember_me)
#         signals.user_logged_in.send(current_app._get_current_object(), user=user)
#     flash("You have been successfully logged in")


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/user/sign-in')
