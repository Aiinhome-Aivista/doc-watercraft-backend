from flask import Flask
from flask_cors import CORS
from middleware.auth_middleware import token_required

from controllers.auth_controller import (login,register,get_loggedin_user,get_all_users)
from controllers.vessel_controller import (
    get_vessels, get_vessel, create_vessel,
    berth_vessel, moor_vessel, survey_vessel, unberth_vessel,
    get_vessel_billing, get_mis_report
)
from controllers.gate_controller import (
    get_gate_entries, create_gate_entry, gate_out,
    create_wbin, create_cargo_operation,update_cargo_operation,create_wbout, get_weighments,get_cargo_operation
)
from controllers.partymasters_controller import (get_partymaster, get_partymasters, create_partymaster, update_partymaster,delete_partymaster)
import os


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

API = "/api/v1"

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

# ─── Vessel Routes ─────────────────────────────────────────────
@app.route(API + '/vessels', methods=['GET'])
@token_required
def route_get_vessels(): return get_vessels()

@app.route(API + '/vessels', methods=['POST'])
@token_required
def route_create_vessel(): return create_vessel()

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

@app.route(API + '/vessels/<int:vessel_id>/billing', methods=['GET'])
@token_required
def route_vessel_billing(vessel_id): return get_vessel_billing(vessel_id)

@app.route(API + '/mis/report', methods=['GET'])
@token_required
def route_mis_report(): return get_mis_report()

# ─── Gate Entry Routes ──────────────────────────────────────────
@app.route(API + '/gate-entries', methods=['GET'])
@token_required
def route_get_gate_entries(): return get_gate_entries()

@app.route(API + '/gate-entries', methods=['POST'])
@token_required
def route_create_gate_entry(): return create_gate_entry()

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
