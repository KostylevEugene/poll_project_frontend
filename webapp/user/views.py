from flask import Blueprint, flash, jsonify, make_response, redirect, \
    render_template, request, session, url_for
from flask_jwt_extended import set_access_cookies
from webapp.config import BACKEND_PORT
from webapp.forms import RegisterForm, SigningInForm
import bcrypt
import requests

blueprint = Blueprint('user', __name__, url_prefix='/users')

salt = bcrypt.gensalt()
expiration_time = 20000

cookies = {'access_token_cookie': ""}


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
        return jsonify({'msg': "method not allowed"}), 405


@blueprint.route('/log', methods=['GET', 'POST'])
def to_sign_in():

    form = SigningInForm()

    session['username'] = "guest"

    global cookies

    if request.method == 'POST' and form.validate():
        url_parts = request.url.partition(f":5001")
        resp = requests.post(f'{url_parts[0]}:{BACKEND_PORT}/{url_parts[2]}',
                             json={'email': form.email.data,
                                   'password': form.password.data,
                                   })
        print(f'{url_parts[0]}:{BACKEND_PORT}/{url_parts[2]}')
        if resp.status_code > 202:
            flash(f"{resp.json()['msg']}")
            return render_template('signing_in.html', form=form)

        session['username'] = form.email.data

        respon = make_response(redirect(url_for('poll.get_mypolls')))

        cookies = {'access_token_cookie': request.cookies.get('access_token')}

        set_access_cookies(respon, resp.json()["JWT"])
        respon.set_cookie('access_token', resp.json()["JWT"])
        return respon

    if request.method == 'GET':
        return render_template('signing_in.html', form=form)

    if request.method == 'OPTIONS':
        return jsonify({'msg': 'Allow GET, POST methods'}), 200

    else:
        return jsonify({"method not allowed"}), 405