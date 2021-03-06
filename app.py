from flask import (
    Flask,
    request,
    jsonify,
    abort,
    render_template,
    redirect,
    url_for,
    session)

import json
from flask_cors import CORS

from models import setup_db, Gnss, Signal
from auth import AuthError, requires_auth

from six.moves.urllib.parse import urlencode

import os
import sys


def create_app(test_config=None):
    ''' Function provides the all endpoints required
    by the flask app (including RBAC for each endpoint)
    and returns the app to be run on a WSGI platform.'''

    app = Flask(__name__)

    app.secret_key = os.environ['APP_SECRET_KEY']
    CLIENT_ID = os.environ['CLIENT_ID']
    AUTH0_BASE_URL = 'https://' + os.environ['AUTH0_DOMAIN']
    IDENTIFIER = os.environ['API_AUDIENCE']

    setup_db(app)

    # Note: Use caution when using CORS:
    # https://www.pivotpointsecurity.com/blog/cross-origin-resource-sharing-security/
    CORS(app)

    # -----------------------------------------------------------------------------------------------------------

    @app.after_request
    # After a request is received, run this after_request method
    def after_request(response):
        '''Defines response headers after every HTML request.'''

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

        return redirect(f'{AUTH0_BASE_URL}/authorize?audience={IDENTIFIER}' +
                        f'&response_type=token&client_id={CLIENT_ID}' +
                        f'&redirect_uri=' +
                        url_for('loggedin', _external=True))

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
    @requires_auth('get:signals')
    def get_gnss_signals(payload):
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
    @requires_auth('post:gnss')
    def create_gnss(payload):
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

        except SQLAlchemyError as e:
            error = True
            new_gnss.cancel()
            new_gnss.close()
            print(sys.exc_info())
            print(e)

        if error:
            abort(422)

        else:
            return jsonify({'success': True, 'gnss': [new_gnss.format()]})

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/gnss-signals', methods=['POST'])
    @requires_auth('post:signal')
    def create_gnss_signal(payload):
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

        except SQLAlchemyError as e:
            error = True
            new_gnss_signal.cancel()
            new_gnss_signal.close()
            print(sys.exc_info())
            print(e)

        if error:
            abort(422)

        else:
            return jsonify({'success': True,
                            'signal': [new_gnss_signal.format()]})

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/gnss/<int:gnss_id>', methods=['PATCH'])
    @requires_auth('patch:gnss')
    def update_gnss(payload, gnss_id):
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

        except SQLAlchemyError as e:
            error = True
            gnss_from_db.cancel()
            gnss_from_db.close()
            print(sys.exc_info())
            print(e)

        if error:
            abort(422)

        else:
            return jsonify({'success': True, 'gnss': [gnss_from_db.format()]})

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/gnss-signals/<int:signal_id>', methods=['PATCH'])
    @requires_auth('patch:signal')
    def update_gnss_signal(payload, signal_id):
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

        except SQLAlchemyError as e:
            error = True
            gnss_from_db.cancel()
            gnss_from_db.close()
            print(sys.exc_info())
            print(e)

        if error:
            abort(422)

        else:
            return jsonify({'success': True,
                            'signal': [gnss_signal_from_db.format()]})

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/gnss/<int:gnss_id>', methods=['DELETE'])
    @requires_auth('delete:gnss')
    def delete_gnss(payload, gnss_id):
        '''Deletes an existing GNSS ID.'''

        if request.method != 'DELETE':
            abort(405)

        error = False

        gnss_to_delete = Gnss.query.get(gnss_id)

        if gnss_to_delete is not None:

            try:
                gnss_to_delete.delete()

            except SQLAlchemyError as e:
                error = True
                gnss_to_delete.cancel()
                gnss_to_delete.close()
                print(sys.exc_info())
                print(e)

            if error:
                abort(422)
            else:
                return jsonify({'success': True, 'delete': gnss_id})

        else:
            abort(404)

    # -----------------------------------------------------------------------------------------------------------

    @app.route('/gnss-signals/<int:signal_id>', methods=['DELETE'])
    @requires_auth('delete:signal')
    def delete_gnss_signal(payload, signal_id):
        '''Deletes an existing GNSS signal.'''

        if request.method != 'DELETE':
            abort(405)

        error = False

        gnss_signal_to_delete = Signal.query.get(signal_id)

        if gnss_signal_to_delete is not None:

            try:
                gnss_signal_to_delete.delete()

            except SQLAlchemyError as e:
                error = True
                gnss_signal_to_delete.cancel()
                gnss_signal_to_delete.close()
                print(sys.exc_info())
                print(e)

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
        '''Provides the response for a 400 error.'''

        return jsonify({'success': False,
                        'error': 400,
                        'message': 'Bad request'}), 400

    @app.errorhandler(404)
    def not_found(error):
        '''Provides the response for a 404 error.'''

        return jsonify({'success': False,
                        'error': 404,
                        'message': 'Not found'}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        '''Provides the response for a 405 error.'''

        return jsonify({'success': False,
                        'error': 405,
                        'message': 'Method not allowed'}), 405

    @app.errorhandler(422)
    def unprocessable(error):
        '''Provides the response for a 422 error.'''

        return jsonify({'success': False,
                        'error': 422,
                        'message': 'Not processable'}), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        '''Provides the response for a 500 error.'''

        return jsonify({'success': False,
                        'error': 500,
                        'message': 'Internal server error'}), 500

    @app.errorhandler(AuthError)
    def auth_error(e):
        '''Provides the response for an authentication error.'''

        return jsonify({'success': False,
                        'error': e.status_code,
                        'message': e.error['description']}), e.status_code

    # -----------------------------------------------------------------------------------------------------------

    return app
