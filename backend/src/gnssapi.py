from flask import Flask, request, jsonify, abort, render_template, redirect, url_for, session
import json
from flask_cors import CORS

# TODO: .database.models doesn't work with test, database.models does
from database.models import setup_db, Gnss, Signal
from auth.auth import AuthError, requires_auth

from six.moves.urllib.parse import urlencode

import sys


def create_app(test_config=None):

    app = Flask(__name__)
    app.secret_key = 'geomatics'
    setup_db(app)
    CORS(app)

    CLIENT_ID = 'nHZZYK1rvE5AHo5twcLgvushH9vbxiA0'
    AUTH0_BASE_URL = 'https://cbhuber.us.auth0.com'
    IDENTIFIER = 'gnss'

    # -----------------------------------------------------------------------------------------------------------

    @app.after_request
    # After a request is received, run this after_request method
    def after_request(response):

        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')

        return response

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/')
    # Does not need @requires_auth decoartor as it is a public endpoint
    def index():
        '''Returns the main index page.'''

        if request.method != 'GET':
            abort(405)

        return render_template('index.html')

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/login')
    # Does not need @requires_auth decoartor as it is a public endpoint
    def login():
        '''Route for the log in page.'''

        if request.method != 'GET':
            abort(405)

        return redirect(f'{AUTH0_BASE_URL}/authorize?audience={IDENTIFIER}&response_type=token&client_id={CLIENT_ID}&redirect_uri=' + url_for('loggedin', _external=True))

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/logout')
    # Does not need @requires_auth decoartor as it is a public endpoint
    def logout():
        '''Route for the log out page.'''

        if request.method != 'GET':
            abort(405)

        # Clear session stored data
        session.clear()

        # Redirect user to logout endpoint
        params = {'returnTo': url_for(
            'loggedout', _external=True), 'client_id': f'{CLIENT_ID}'}

        return redirect(AUTH0_BASE_URL + '/v2/logout?' + urlencode(params))

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/loggedin')
    # Does not need @requires_auth decoartor as it is a public endpoint
    def loggedin():
        '''Page to redirect to after logging in.'''

        if request.method != 'GET':
            abort(405)

        return render_template('loggedin.html')

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/loggedout')
    # Does not need @requires_auth decoartor as it is a public endpoint
    def loggedout():
        '''Page to redirect to after logging out.'''

        if request.method != 'GET':
            abort(405)

        return render_template('loggedout.html')

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/gnss')
    # Does not need @requires_auth decoartor as it is a public endpoint
    def get_gnss():
        '''Gets a GNSS API.'''

        if request.method != 'GET':
            abort(405)

        all_gnss_from_db = Gnss.query.all()

        if len(all_gnss_from_db) == 0:
            abort(404)

        result = {}
        result['success'] = True
        result['gnss'] = [gnss.format() for gnss in all_gnss_from_db]

        return jsonify(result)

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/gnss-signals')
    # @requires_auth('TBD')
    # def get_gnss_signals(payload):
    def get_gnss_signals():
        '''Gets GNSS signals API.'''

        if request.method != 'GET':
            abort(405)

        all_gnss_signals_from_db = Signal.query.all()

        if len(all_gnss_signals_from_db) == 0:
            abort(404)

        result = {}
        result['success'] = True
        result['signal'] = [signal.format()
                            for signal in all_gnss_signals_from_db]

        return jsonify(result)

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/gnss', methods=['POST'])
    # @requires_auth('TBD')
    # def create_gnss(payload):
    def create_gnss():
        '''Creates a new GNSS.'''

        if request.method != 'POST':
            abort(405)

        gnss_data = request.get_json()

        if not gnss_data:
            abort(400)

        error = False

        try:
            new_gnss = Gnss(**gnss_data)
            new_gnss.insert()

        except:
            error = True
            new_gnss.cancel()
            new_gnss.close()
            print(sys.exc_info())

        if error:
            abort(422)

        else:
            return jsonify({'success': True, 'gnss': [new_gnss.format()]})

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/gnss-signals', methods=['POST'])
    # @requires_auth('TBD')
    # def create_gnss_signal(payload):
    def create_gnss_signal():
        '''Creates a new GNSS signal.'''

        if request.method != 'POST':
            abort(405)

        gnss_signal_data = request.get_json()

        if not gnss_signal_data:
            abort(400)

        error = False

        try:
            new_gnss_signal = Signal(**gnss_signal_data)
            new_gnss_signal.insert()

        except:
            error = True
            new_gnss_signal.cancel()
            new_gnss_signal.close()
            print(sys.exc_info())

        if error:
            abort(422)

        else:
            return jsonify({'success': True, 'signal': [new_gnss_signal.format()]})

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/gnss/<int:gnss_id>', methods=['PATCH'])
    # @requires_auth('TBD')
    # def update_gnss(payload, gnss_id):
    def update_gnss(gnss_id):
        '''Updates an existing GNSS ID.'''

        if request.method != 'PATCH':
            abort(405)

        gnss_from_db = Gnss.query.get(gnss_id)

        if not gnss_from_db:
            abort(404)

        gnss_data = request.get_json()

        if not gnss_data:
            abort(400)

        error = False

        try:

            if 'name' in gnss_data:
                gnss_from_db.name = gnss_data['name']

            if 'owner' in gnss_data:
                gnss_from_db.owner = gnss_data['owner']

            if 'num_satellites' in gnss_data:
                gnss_from_db.num_satellites = gnss_data['num_satellites']

            if 'num_frequencies' in gnss_data:
                gnss_from_db.num_frequencies = gnss_data['num_frequencies']

        except:
            error = True
            gnss_from_db.cancel()
            gnss_from_db.close()
            print(sys.exc_info())

        if error:
            abort(422)

        else:
            return jsonify({'success': True, 'gnss': [gnss_from_db.format()]})

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/gnss-signals/<int:signal_id>', methods=['PATCH'])
    # @requires_auth('TBD')
    # def update_gnss_signal(payload, signal_id):
    def update_gnss_signal(signal_id):
        '''Updates an existing GNSS signal ID.'''

        if request.method != 'PATCH':
            abort(405)

        gnss_signal_from_db = Signal.query.get(signal_id)

        if not gnss_signal_from_db:
            abort(404)

        signal_data = request.get_json()

        if not signal_data:
            abort(400)

        error = False

        try:

            if 'signal' in signal_data:
                gnss_signal_from_db.signal = signal_data['signal']

            if 'gnss_id' in signal_data:
                gnss_signal_from_db.gnss_id = signal_data['gnss_id']

        except:
            error = True
            gnss_from_db.cancel()
            gnss_from_db.close()
            print(sys.exc_info())

        if error:
            abort(422)

        else:
            return jsonify({'success': True, 'signal': [gnss_signal_from_db.format()]})

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/gnss/<int:gnss_id>', methods=['DELETE'])
    # @requires_auth('TBD')
    # def delete_gnss(payload, gnss_id):
    def delete_gnss(gnss_id):
        '''Deletes an existing GNSS ID.'''

        if request.method != 'DELETE':
            abort(405)

        error = False

        gnss_to_delete = Gnss.query.get(gnss_id)

        if gnss_to_delete is not None:

            try:
                gnss_to_delete.delete()

            except:
                error = True
                gnss_to_delete.cancel()
                gnss_to_delete.close()
                print(sys.exc_info())

            if error:
                abort(422)
            else:
                return jsonify({'success': True, 'delete': gnss_id})

        else:
            abort(404)

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/gnss-signals/<int:signal_id>', methods=['DELETE'])
    # @requires_auth('TBD')
    # def delete_gnss_signal(payload, signal_id):
    def delete_gnss_signal(signal_id):
        '''Deletes an existing GNSS signal TBD.'''

        if request.method != 'DELETE':
            abort(405)

        error = False

        gnss_signal_to_delete = Signal.query.get(signal_id)

        if gnss_signal_to_delete is not None:

            try:
                gnss_signal_to_delete.delete()

            except:
                error = True
                gnss_signal_to_delete.cancel()
                gnss_signal_to_delete.close()
                print(sys.exc_info())

            if error:
                abort(422)
            else:
                return jsonify({'success': True, 'delete': signal_id})

        else:
            abort(404)

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

    return app
