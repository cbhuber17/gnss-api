from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS

from .database.models import setup_db, Gnss, Signal
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# ROUTES

# -----------------------------------------------------------------------------------------------------------


@app.route('/')
# Does not need @requires_auth decoartor as it is a public endpoint
def get_gnss():
    '''Gets a GNSS TBD.'''

    # TODO:
    # if request.method != 'GET':
    #     abort(405)

    all_gnss_from_db = Gnss.query.all()

    # TODO:
    # if len(all_drinks_from_db) == 0:
    #     abort(404)

    result = {}
    result['success'] = True
    result['gnss'] = [gnss.format() for gnss in all_gnss_from_db]

    return jsonify(result)

# -----------------------------------------------------------------------------------------------------------


@app.route('/gnss-signals')
# @requires_auth('TBD')
# def get_gnss_signals(payload):
def get_gnss_signals():
    '''Gets GNSS signals TBD.'''

    # TODO:
    # if request.method != 'GET':
    #     abort(405)

    all_gnss_signals_from_db = Signal.query.all()

    # TODO:
    # if len(all_drinks_from_db) == 0:
    #     abort(404)

    result = {}
    result['success'] = True
    result['signal'] = [signal.format() for signal in all_gnss_signals_from_db]

    return jsonify(result)

# -----------------------------------------------------------------------------------------------------------


@app.route('/gnss', methods=['POST'])
# @requires_auth('TBD')
# def create_gnss(payload):
def create_gnss():
    '''Creates a new GNSS TBD.'''

    # TODO: Error handling

    gnss_data = request.get_json()

    print(gnss_data)

    new_gnss = Gnss(**gnss_data)

    # TODO: Add to db and error handling

    print(new_gnss.format())

    return jsonify({'success': True, 'gnss': [new_gnss.format()]})

# -----------------------------------------------------------------------------------------------------------


@app.route('/gnss-signals', methods=['POST'])
# @requires_auth('TBD')
# def create_gnss_signal(payload):
def create_gnss_signal():
    '''Creates a new GNSS signal TBD.'''

    # TODO: Error handling

    gnss_signal_data = request.get_json()

    print(gnss_signal_data)

    new_gnss_signal = Signal(**gnss_signal_data)

    # TODO: Add to db and error handling

    print(new_gnss_signal.format())

    return jsonify({'success': True, 'signal': [new_gnss_signal.format()]})

# -----------------------------------------------------------------------------------------------------------


@app.route('/gnss/<int:gnss_id>', methods=['PATCH'])
# @requires_auth('TBD')
# def update_gnss(payload, gnss_id):
def update_gnss(gnss_id):
    '''Updates an existing GNSS TBD.'''

    # TODO: Error handling

    gnss_from_db = Gnss.query.get(gnss_id)

    gnss_data = request.get_json()
    print(gnss_data)

    if 'name' in gnss_data:
        gnss_from_db.name = gnss_data['name']

    if 'owner' in gnss_data:
        gnss_from_db.owner = gnss_data['owner']

    if 'num_satellites' in gnss_data:
        gnss_from_db.num_satellites = gnss_data['num_satellites']

    if 'num_frequencies' in gnss_data:
        gnss_from_db.num_frequencies = gnss_data['num_frequencies']

    # TODO: Add to db and error handling

    print(gnss_from_db.format())

    return jsonify({'result': True, 'gnss': [gnss_from_db.format()]})

# -----------------------------------------------------------------------------------------------------------


@app.route('/gnss-signals/<int:signal_id>', methods=['PATCH'])
# @requires_auth('TBD')
# def update_gnss_signal(payload, signal_id):
def update_gnss_signal(signal_id):
    '''Updates an existing GNSS signal TBD.'''

    # TODO: Error handling

    gnss_signal_from_db = Signal.query.get(signal_id)

    signal_data = request.get_json()
    print(signal_data)

    if 'signal' in signal_data:
        gnss_signal_from_db.signal = signal_data['signal']

    if 'gnss_id' in signal_data:
        gnss_signal_from_db.gnss_id = signal_data['gnss_id']

    # TODO: Add to db and error handling

    print(gnss_signal_from_db.format())

    return jsonify({'result': True, 'signal': [gnss_signal_from_db.format()]})

# -----------------------------------------------------------------------------------------------------------


@app.route('/gnss/<int:gnss_id>', methods=['DELETE'])
# @requires_auth('TBD')
# def delete_gnss(payload, gnss_id):
def delete_gnss(gnss_id):
    '''Deletes an existing GNSS TBD.'''

    gnss_to_delete = Gnss.query.get(gnss_id)

    # TODO: Implement and error check

    return jsonify({'success': True, 'delete': gnss_id})

# -----------------------------------------------------------------------------------------------------------


@app.route('/gnss-signals/<int:signal_id>', methods=['DELETE'])
# @requires_auth('TBD')
# def delete_gnss_signal(payload, signal_id):
def delete_gnss_signal(signal_id):
    '''Deletes an existing GNSS signal TBD.'''

    gnss_signal_to_delete = Signal.query.get(signal_id)

    # TODO: Implement and error check

    return jsonify({'success': True, 'delete': signal_id})

# -----------------------------------------------------------------------------------------------------------

# TODO: Implement search method

# -----------------------------------------------------------------------------------------------------------


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'success': False, 'error': 400, 'message': 'Bad request'}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 404, 'message': 'Not found'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'success': False, 'error': 405, 'message': 'Method not allowed'}), 405


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({'success': False, 'error': 422, 'message': 'Not processable'}), 422


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'success': False, 'error': 500, 'message': 'Internal server error'}), 500


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({'success': False, 'error': error.status_code, 'message': error.error['description']}), error.status_code

# -----------------------------------------------------------------------------------------------------------
