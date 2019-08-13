from flask import (
    Blueprint,
    redirect,
    request,
    flash,
    url_for,
    render_template,
    current_app, jsonify, json)
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user)

from ..user.decorators import (role_required)

from lib.safe_next_url import safe_next_url
from .decorators import anonymous_required
from .models import User
from .forms import (
    LoginForm,
    SignupForm)

from ...extensions import db, csrf

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/', methods=['GET'])
def landing_page():
    return redirect(url_for('page.home'))


@user.route('/signup', methods=['GET', 'POST'])
@anonymous_required()
def signup():
    signup_form = SignupForm()

    if signup_form.validate_on_submit():
        u = User()

        signup_form.populate_obj(u)
        u.password = User.encrypt_password(request.form.get('password'))
        if u.email in current_app.config['TECH_SUPPORT']:
            u.role = 'tech support'

        db.session.add(u)
        db.session.commit()

        if login_user(u):
            flash('Awesome, thanks for signing up!')
            return redirect(url_for('page.home'))

    return render_template('signup.html', signup=signup_form)


@user.route('/signin', methods=['GET', 'POST'])
@anonymous_required()
def signin():
    form = LoginForm(next=request.args.get('next'))

    if form.validate_on_submit():
        u = User.find_by_identity(request.form.get('email'))

        if u and u.authenticated(password=request.form.get('password')):
            if login_user(u, remember=False) and u.is_active():
                u.update_activity_tracking(request.remote_addr)

                # Handle optionally redirecting to the next URL safely.
                next_url = request.form.get('next')
                if next_url:
                    return redirect(safe_next_url(next_url))

                return redirect(url_for('page.home'))
            else:
                flash('This account has been disabled.', 'error')
        else:
            flash('Identity or password is incorrect.', 'error')

    return render_template('signin.html', signin=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('user.signin'))


