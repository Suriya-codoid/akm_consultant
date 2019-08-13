from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template, request, jsonify)
from flask_login import (
    login_required, current_user)
from ...extensions import db, csrf
from datatables import ColumnDT, DataTables

from ..user.models import Application_details

page = Blueprint('page', __name__, template_folder='templates')

# this is the landing page, both users are land into this page and contents are differ by user wise
@page.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        app_details = Application_details()
        email = request.form['email']
        mobile_number = request.form['mobile-number']
        print(Application_details.get_details(email, mobile_number=None))
        if Application_details.get_details(email, mobile_number=None) is not None:
            status = "fail"
            message = "Application with this E-mail Already submitted"
        elif Application_details.get_details(email=None, mobile_number=mobile_number) is not None:
            status = "fail"
            message = "Application with this mobile Number Already submitted"
        elif Application_details.get_details(email, mobile_number) is not None:
            status = "fail"
            message = "Application with this mobile Number and E-mail Already submitted"
        else:
            app_details.full_name = request.form['full-name']
            app_details.middle_name = request.form['middle-name']
            app_details.last_name = request.form['last-name']
            app_details.current_address = request.form['current-address']
            app_details.street_address = request.form['street-address']
            app_details.city = request.form['district']
            app_details.position = request.form['position']
            app_details.state = request.form['state']
            app_details.email = request.form['email']
            app_details.mobile_number = request.form['mobile-number']
            app_details.pin_code = request.form['pin-code']
            db.session.add(app_details)
            db.session.commit()
            status = "pass"
            message = "Successfully Submitted"

        return jsonify({"status": status, "message": message})

    return render_template('page/home.html')

# this function is list the Application and only visible by tech support
@page.route('/listDetails')
@login_required
def get_appliaction_details():
    columns = [
        ColumnDT(Application_details.id),
        ColumnDT(Application_details.full_name),
        ColumnDT(Application_details.email),
        ColumnDT(Application_details.status)
    ]

    query = db.session.query(Application_details.id, Application_details.full_name, Application_details.email,
                             Application_details.status).select_from(
        Application_details)

    params = request.args.to_dict()

    row_table = DataTables(params, query, columns)

    return jsonify(row_table.output_result())

# this function is used to ACCEPT and REJECT the application. only for tech support
@page.route('/changeStatus', methods=['POST'])
@login_required
def change_status():
    table_id = request.form['id']
    status = request.form['status']
    get_row = Application_details.get_row(table_id)
    if get_row.status == 1:
        get_row.status = 0
    else:
        get_row.status = 1

    return jsonify({"status": "pass", "message": "Application has been successfully " + status + ""})

# this function is used to view the application details
@page.route('/getDetails', methods=['GET'])
@login_required
def get_details():
    table_id = request.args.get('id')
    get_row = Application_details.get_row(table_id)
    details = [{"full-name": get_row.full_name, "middle-name": get_row.middle_name, "last-name": get_row.last_name,
            "current-address": get_row.current_address, "street_address": get_row.street_address, "district": get_row.city,
            "state": get_row.state, "pin-code": get_row.pin_code, "email": get_row.email, "mobile-number": get_row.mobile_number,
            "position": get_row.position}]
    return jsonify({"details": details})
