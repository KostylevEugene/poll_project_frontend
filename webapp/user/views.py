from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
# from webapp.queries import *
from webapp.config import BACKEND_PORT
from webapp.forms import RegisterForm
import bcrypt
import requests

blueprint = Blueprint('user', __name__, url_prefix='/users')

salt = bcrypt.gensalt()
expiration_time = 20000


@blueprint.route('/registration', methods=['GET', 'POST'])
def to_sign_up():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        url_parts = request.url.partition(f":5001")
        resp = requests.post(f'{url_parts[0]}:{BACKEND_PORT}/{url_parts[2]}',
                             json={'name': form.name.data,
                                   'email': form.email.data,
                                   'password': form.password.data,
                                   'valid_password': form.valid_password.data,
                                   })
        if resp.status_code > 202:
            flash(f"{resp.json()['msg']}")
            return render_template('register.html', form=form)
        flash(f"{resp.json()['msg']}")
        return redirect(url_for('user.to_sign_in'))

    if request.method == 'GET':
        return render_template('registration.html', form=form)

    if request.method == 'OPTIONS':
        return jsonify({'msg': 'Allow GET, POST methods'}), 200

    else:
        return jsonify({'msg':"method not allowed"}), 405


@blueprint.route('/log', methods=['GET', 'POST'])
def to_sign_in():
    # session['username'] = 'guest'
    #
    # if request.method == 'POST':
    #     email = request.json['email']
    #     password = request.json['password']
    #
    #     old_user = signed_in_user(email)
    #
    #     if old_user != email:
    #         return jsonify({'msg': 'There is no such email'}), 201
    #
    #     else:
    #         existed_password = get_password_by_email(email)
    #         if bcrypt.checkpw(password.encode('utf8'), existed_password.encode('utf8')):
    #             session['username'] = email
    #             refresh_token = create_refresh_token(identity=email,
    #                                                  expires_delta=datetime.timedelta(seconds=expiration_time))
    #             access_token = create_access_token(identity=email,
    #                                                expires_delta=datetime.timedelta(seconds=expiration_time))
    #             response = jsonify({'login': True, 'JWT': access_token, 'refresh_token': refresh_token})
    #             # app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    #             response.status_code = 200
    #             return response
    #         else:
    #             jsonify({'msg': 'Wrong password'}), 407

    if request.method == 'GET':
        return jsonify({'msg': 'Login page'}), 200

    if request.method == 'OPTIONS':
        return jsonify({'msg': 'Allow GET, POST methods'}), 200

    else:
        return jsonify({"method not allowed"}), 405