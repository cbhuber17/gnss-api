from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS

from .database.models import setup_db, Gnss, Signal

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

# @app.route('/gnss', methods=['POST'])
# @requires_auth('TBD')
# def create_gnss(payload):
#     '''Creates a new GNSS TBD.'''

#     return jsonify(result)

# -----------------------------------------------------------------------------------------------------------

# @app.route('/gnss-signals', methods=['POST'])
# @requires_auth('TBD')
# def create_gnss_signal(payload):
#     '''Creates a new GNSS signal TBD.'''

#     return jsonify(result)

# -----------------------------------------------------------------------------------------------------------

# @app.route('/gnss/<int:gnss_id>', methods=['PATCH'])
# @requires_auth('TBD')
# def update_gnss(payload, gnss_id):
#     '''Updates an existing GNSS TBD.'''

#     return jsonify(result)

# -----------------------------------------------------------------------------------------------------------

# @app.route('/gnss-signals/<int:signal_id>', methods=['PATCH'])
# @requires_auth('TBD')
# def update_gnss_signal(payload, signal_id):
#     '''Updates an existing GNSS signal TBD.'''

#     return jsonify(result)

# -----------------------------------------------------------------------------------------------------------

# @app.route('/gnss/<int:gnss_id>', methods=['DELETE'])
# @requires_auth('TBD')
# def delete_gnss(payload, gnss_id):
#     '''Deletes an existing GNSS TBD.'''

#     return jsonify(result)

# -----------------------------------------------------------------------------------------------------------

# @app.route('/gnss-signals/<int:signal_id>', methods=['DELETE'])
# @requires_auth('TBD')
# def delete_gnss_signal(payload, signal_id):
#     '''Deletes an existing GNSS signal TBD.'''

#     return jsonify(result)

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

# TODO: Implement AuthError
# @app.errorhandler(AuthError)
# def auth_error(error):
#     return jsonify({'success': False, 'error': error.status_code, 'message': error.error['description']}), error.status_code

# -----------------------------------------------------------------------------------------------------------
