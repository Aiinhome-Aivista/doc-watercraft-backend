from flask import Flask
from flask_cors import CORS
from middleware.auth_middleware import token_required

from controllers.auth_controller import (login,register,get_loggedin_user,get_all_users,update_access_rights,get_access_rights,change_password,admin_change_user_password,delete_user)
from controllers.vehicle_controller import (create_vehicle, get_vehicles, get_vehicle, update_vehicle, delete_vehicle, toggle_vehicle_status)
from controllers.vessel_controller import (
    get_vessels, get_vessel, create_vessel,
    berth_vessel, moor_vessel, survey_vessel, unberth_vessel,
    get_vessel_billing, get_mis_report,get_rates_by_vessel,update_rate,update_vessel,
    get_vessel_names, get_vehicle_movement_report
)
from controllers.gate_controller import (
    get_gate_entries, create_gate_entry, gate_out,
    create_wbin, create_cargo_operation,update_cargo_operation,create_wbout, get_weighments,get_cargo_operation,
    update_gate_entry, get_gate_in_numbers
)
from controllers.partymasters_controller import (get_partymaster, get_partymasters, create_partymaster, update_partymaster,delete_partymaster)

from controllers.billing_controller import (get_vessels_for_billing,generate_bill,pdf_bill_generator,download_bill_pdf,get_all_bills,update_bill,delete_bill)
from controllers.export_controller import export_full_report, download_export, export_vehicle_movement_report, export_bills_report
import os


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

API = "/api/v1"

@app.route("/")
def health():return "API is running"

# ─── Public Routes ──────────────────────────────────────────────
@app.route(API + '/login', methods=['POST'])
def route_login(): return login()

@app.route(API + '/register', methods=['POST'])
def route_register():return register()

# ─── User Routes ────────────────────────────────────────────────
@app.route(API +'/logged-in-user', methods=['GET'])
@token_required
def route_loggedin_user(): return get_loggedin_user()

@app.route(API + '/users', methods=['GET'])
@token_required
def route_get_users(): return get_all_users()

@app.route(API + '/users/<int:user_id>', methods=['DELETE'])
@token_required
def route_delete_user(user_id): return delete_user(user_id)

@app.route(API + '/change-password', methods=['POST'])
@token_required
def route_change_password():return change_password()

@app.route(API + '/change-password/<int:user_id>', methods=['POST'])
@token_required
def route_admin_change_password(user_id):return admin_change_user_password(user_id)

# ─── Access Rights Routes ───────────────────────────────────────
@app.route(API + '/access-rights/<int:user_id>', methods=['POST'])
@token_required
def route_update_access_rights(user_id): return update_access_rights(user_id)

@app.route(API + '/access-rights/<int:user_id>', methods=['GET'])
@token_required
def route_get_access_rights(user_id): return get_access_rights(user_id)

# ─── Party Masters Routes ───────────────────────────────────────
@app.route(API + '/partymasters', methods=['GET'])
@token_required
def route_get_partymasters(): return get_partymasters()

@app.route(API + '/partymasters/<int:partymaster_id>', methods=['GET'])
@token_required
def route_get_partymaster(partymaster_id):return get_partymaster(partymaster_id)

@app.route(API + '/partymasters', methods=['POST'])
@token_required
def route_create_partymaster(): return create_partymaster()

@app.route(API + '/partymasters/<int:partymaster_id>', methods=['POST'])
@token_required
def route_update_partymaster(partymaster_id):return update_partymaster(partymaster_id)

@app.route(API + '/partymasters/<int:partymaster_id>', methods=['DELETE'])
@token_required
def route_delete_partymaster(partymaster_id):return delete_partymaster(partymaster_id)

# ─── vehicles Masters Routes ─────────────────────────────────────
@app.route(API + '/vehicles', methods=['POST'])
@token_required
def add_vehicle():return create_vehicle()

@app.route(API + '/vehicles', methods=['GET'])
@token_required
def list_vehicles():return get_vehicles()

@app.route(API + '/vehicles/<int:vehicle_id>', methods=['GET'])
@token_required
def single_vehicle(vehicle_id):return get_vehicle(vehicle_id)

@app.route(API + '/vehicles/<int:vehicle_id>', methods=['PUT'])
@token_required
def edit_vehicle(vehicle_id):return update_vehicle(vehicle_id)

@app.route(API + '/vehicles/<int:vehicle_id>', methods=['DELETE'])
@token_required
def remove_vehicle(vehicle_id):return delete_vehicle(vehicle_id)

@app.route(API + '/vehicles/<int:vehicle_id>/toggle', methods=['PATCH'])
@token_required
def toggle_vehicle(vehicle_id):return toggle_vehicle_status(vehicle_id)

# ─── Vessel Routes ─────────────────────────────────────────────
@app.route(API + '/vessels', methods=['GET'])
@token_required
def route_get_vessels(): return get_vessels()

@app.route(API + '/vessels/names', methods=['GET'])
@token_required
def route_get_vessel_names(): return get_vessel_names()

@app.route(API + '/vessels', methods=['POST'])
@token_required
def route_create_vessel(): return create_vessel()

@app.route(API + '/vessels/<int:vessel_id>', methods=['POST'])
def update_vessel_route(vessel_id):return update_vessel(vessel_id)

@app.route(API + '/vessels/<int:vessel_id>', methods=['GET'])
@token_required
def route_get_vessel(vessel_id): return get_vessel(vessel_id)

@app.route(API + '/vessels/<int:vessel_id>/berth', methods=['POST'])
@token_required
def route_berth_vessel(vessel_id): return berth_vessel(vessel_id)

@app.route(API + '/vessels/<int:vessel_id>/moor', methods=['POST'])
@token_required
def route_moor_vessel(vessel_id): return moor_vessel(vessel_id)

@app.route(API + '/vessels/<int:vessel_id>/survey', methods=['POST'])
@token_required
def route_survey_vessel(vessel_id): return survey_vessel(vessel_id)

@app.route(API + '/vessels/<int:vessel_id>/unberth', methods=['POST'])
@token_required
def route_unberth_vessel(vessel_id): return unberth_vessel(vessel_id)

# Billing & MIS Routes
@app.route(API + '/rates/<int:vessel_id>', methods=['GET'])
@token_required
def route_rates_by_vessel(vessel_id):return get_rates_by_vessel(vessel_id)

@app.route(API + "/billing/vessels", methods=["POST"])
@token_required
def route_billing_vessels():return get_vessels_for_billing()

@app.route(API + "/billing/generate", methods=["POST"])
@token_required
def route_generate_bill():return generate_bill()

@app.route(API + '/rates/<int:vessel_id>/<int:rate_id>', methods=['POST'])
@token_required
def route_vessel_billing(vessel_id, rate_id): return update_rate(vessel_id, rate_id)

# @app.route(API + '/mis/report', methods=['GET'])
# @token_required
# def route_mis_report(): return get_mis_report()

@app.route(API + '/reports/vehicle-movement', methods=['GET'])
@token_required
def route_vehicle_movement_report(): return get_vehicle_movement_report()

@app.route(API +'/pdf-bill', methods=['POST'])
def pdf_bill():return pdf_bill_generator()

@app.route(API + '/pdf-bill/<path:filename>', methods=['GET'])
def download_pdf_bill(filename): return download_bill_pdf(filename)

# GET all bills with detailed activity items and vessel names
@app.route(API + '/all_bills', methods=['GET'])
@token_required
def route_get_all_bills(): return get_all_bills()

@app.route(API + '/all_bills/<int:bill_id>', methods=['PUT'])
@token_required
def route_update_bill(bill_id): return update_bill(bill_id)

@app.route(API + '/all_bills/<int:bill_id>', methods=['DELETE'])
@token_required
def route_delete_bill(bill_id): return delete_bill(bill_id)

# ─── Gate Entry Routes ──────────────────────────────────────────
@app.route(API + '/gate-entries', methods=['GET'])
@token_required
def route_get_gate_entries(): return get_gate_entries()

@app.route(API + '/gate-entries/nos', methods=['GET'])
@token_required
def route_get_gate_in_numbers(): return get_gate_in_numbers()

@app.route(API + '/gate-entries', methods=['POST'])
@token_required
def route_create_gate_entry(): return create_gate_entry()

@app.route(API + '/gate-entries/<int:gate_id>', methods=['PUT'])
@token_required
def route_update_gate_entry(gate_id): return update_gate_entry(gate_id)

@app.route(API + '/gate-entries/<int:gate_id>/gate-out', methods=['POST'])
@token_required
def route_gate_out(gate_id): return gate_out(gate_id)

@app.route(API + '/gate-entries/<int:gate_id>/weighments', methods=['GET'])
@token_required
def route_get_weighments(gate_id): return get_weighments(gate_id)

# ─── Weighbridge & Operations Routes ───────────────────────────
@app.route(API + '/wbin', methods=['POST'])
@token_required
def route_create_wbin(): return create_wbin()

@app.route(API + '/cargo-operations/<int:operation_id>', methods=['GET'])
@token_required
def route_get_cargo_operation(operation_id):return get_cargo_operation(operation_id)

@app.route(API + '/cargo-operations', methods=['POST'])
@token_required
def route_create_cargo_operation(): return create_cargo_operation()

@app.route(API + '/cargo-operations/<int:operation_id>', methods=['POST'])
@token_required
def route_update_cargo_operation(operation_id):return update_cargo_operation(operation_id)

@app.route(API + '/wbout', methods=['POST'])
@token_required
def route_create_wbout(): return create_wbout()

# ─── EXPORT & DOWNLOAD ───────────────────────────
@app.route(API + '/export/full-report', methods=['GET'])
@token_required
def route_export_full():return export_full_report()

@app.route(API + '/export/download/<filename>', methods=['GET'])
def route_download_export(filename):return download_export(filename)

@app.route(API + '/export/vehicle-movement', methods=['GET'])
@token_required
def route_export_vehicle_movement(): return export_vehicle_movement_report()

@app.route(API + '/export/bills', methods=['GET'])
@token_required
def route_export_bills(): return export_bills_report()


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
