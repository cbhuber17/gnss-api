import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from gnssapi import create_app
from database.models import setup_db, Gnss, Signal


class GnssTestCase(unittest.TestCase):
    '''Class representing the suite of GNSS API test cases.'''

    def add_gnss_to_db(self):
        '''Populates the db with some GNSS data.'''

        gnss1 = Gnss(name='GPS', owner='USA',
                     num_satellites=32, num_frequencies=3)
        gnss2 = Gnss(name='Galileo', owner='EU',
                     num_satellites=36, num_frequencies=4)
        self.db.session.add(gnss1)
        self.db.session.add(gnss2)

        self.db.session.commit()

    def add_gnss_signals_to_db(self):
        '''Populates the db with some GNSS signal data.'''

        signal1 = Signal(signal='L1 C/A', gnss_id=1)
        signal2 = Signal(signal='L1C', gnss_id=1)
        signal3 = Signal(signal='L2 P(Y)', gnss_id=1)
        signal4 = Signal(signal='L2C', gnss_id=1)
        signal5 = Signal(signal='L5', gnss_id=1)
        signal6 = Signal(signal='E1', gnss_id=2)
        signal7 = Signal(signal='E5A', gnss_id=2)
        signal8 = Signal(signal='E5B', gnss_id=2)
        signal9 = Signal(signal='E5AltBOC', gnss_id=2)
        self.db.session.add(signal1)
        self.db.session.add(signal2)
        self.db.session.add(signal3)
        self.db.session.add(signal4)
        self.db.session.add(signal5)
        self.db.session.add(signal6)
        self.db.session.add(signal7)
        self.db.session.add(signal8)
        self.db.session.add(signal9)

        self.db.session.commit()

    def setUp(self):
        '''Defines the test case variables and initializes the app.'''

        # Capture these bearer tokens after logging in (will be displayed on the page)
        self.client_bearer_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh5VC1aRk1qdkVoaTNRVUJMLW44QiJ9.eyJpc3MiOiJodHRwczovL2NiaHViZXIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZDUwZGRkMDI1NzBjMDA2ZTljNGIxZiIsImF1ZCI6Imduc3MiLCJpYXQiOjE2MDc4MDE5MzAsImV4cCI6MTYwNzg4ODMzMCwiYXpwIjoibkhaWllLMXJ2RTVBSG81dHdjTGd2dXNoSDl2YnhpQTAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpzaWduYWxzIl19.xpbPR1Ua6v02VbaQBsSKNDGcQvz4d6PmxV22Fse_VdEr_NxzQEChD-3qO8U7bQOxnFg40iUwhSf1tkEL7LYEH6K5RM2xuz_7kplrgFzMKXkBEPnkJYET1DiLJCIFthxsZLoc3xNL-pm2DO6AO-iD8iMMoTQpr-A6bmqfzL-n5FUeZr1pa7B3VM4sAdf--3Kbe6QNcAOYED_d4nmbs4dMNKL3sGo7f4jzX0GvJ3kmZmYUjszNEoV49iYAD9nO8DX5IMJIwGXPHob0TUfoH6mqlma35f510jFyWMnCFg2pn_uWMQXGFLzbHPIKCte9zuRM9G37ofr9gf7UsY7DMe7Bvg'
        self.director_bearer_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh5VC1aRk1qdkVoaTNRVUJMLW44QiJ9.eyJpc3MiOiJodHRwczovL2NiaHViZXIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZDUwZDhhYjI3ZDhhMDA2OGE5MTAzNCIsImF1ZCI6Imduc3MiLCJpYXQiOjE2MDc4MDE4NjcsImV4cCI6MTYwNzg4ODI2NywiYXpwIjoibkhaWllLMXJ2RTVBSG81dHdjTGd2dXNoSDl2YnhpQTAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpnbnNzIiwiZGVsZXRlOnNpZ25hbCIsImdldDpzaWduYWxzIiwicGF0Y2g6Z25zcyIsInBhdGNoOnNpZ25hbCIsInBvc3Q6Z25zcyIsInBvc3Q6c2lnbmFsIl19.eBUOWs7MowemhFsXk2Zz9oFHtdjJKTzz1GZ55osOrDpQflnvOEcF551nI0qCfyYLekLXddMdJdPGk6FmLeaahLRZbvdmKb6vENxpuUZbae9ftwSt7OnQniskAdwebyobIPFILjG1b_hIFzU9VWk9gnO2ZWRVpp0x__EAKay08ix0S8KL2ct_sA5lH6W6xg23y91PJyfEe5XnFxLUb5QVso663HdPt3o57i7teMYgM25oJkmIblnUACCc5o4cmJJKE8pQg5YQxOZah4Na16f_RNEu0OuVVU2toyg0WQrVJErI1unkJLtij81iJvmHxZIFIUDO2cS8v8602lQl3eTTRQ'

        self.client_auth_header = {'Authorization': self.client_bearer_token}
        self.director_auth_header = {
            'Authorization': self.director_bearer_token}

        self.app = create_app()
        self.client = self.app.test_client
        # db must exist first!  "createdb -U postgres gnss_test"
        self.database_name = "gnss_test"
        self.database_path = f"postgres://postgres@localhost:5432/{self.database_name}"

        db = setup_db(self.app, self.database_path)
        db.drop_all()
        db.create_all()

        # Binds the app to the current testing context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            self.db.drop_all()
            self.db.create_all()

            # Populate the db for proper unit testing
            self.add_gnss_to_db()
            self.add_gnss_signals_to_db()

    def tearDown(self):
        '''Executes after each test.'''
        pass

    # -----------------------------------------------------------------------------------------------------------

    def test_main_page(self):
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)

    def test_main_page_post(self):
        res = self.client().post('/')

        self.assertEqual(res.status_code, 405)

    # -----------------------------------------------------------------------------------------------------------

    def test_login_page(self):
        res = self.client().get('/login')

        self.assertEqual(res.status_code, 302)

    def test_login_page_post(self):
        res = self.client().post('/login')

        self.assertEqual(res.status_code, 405)

    # -----------------------------------------------------------------------------------------------------------

    def test_logout_page(self):
        res = self.client().get('/logout')

        self.assertEqual(res.status_code, 302)

    def test_logout_page_post(self):
        res = self.client().post('/logout')

        self.assertEqual(res.status_code, 405)

    # -----------------------------------------------------------------------------------------------------------

    def test_loggedin_page(self):
        res = self.client().get('/loggedin')

        self.assertEqual(res.status_code, 200)

    def test_loggedin_page_post(self):
        res = self.client().post('/loggedin')

        self.assertEqual(res.status_code, 405)

    # -----------------------------------------------------------------------------------------------------------

    def test_loggedout_page(self):
        res = self.client().get('/loggedout')

        self.assertEqual(res.status_code, 200)

    def test_loggedout_page_post(self):
        res = self.client().post('/loggedout')

        self.assertEqual(res.status_code, 405)

    # -----------------------------------------------------------------------------------------------------------

    def test_get_request_gnss(self):
        res = self.client().get('/gnss')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

    def test_get_request_gnss_director(self):
        res = self.client().get('/gnss', headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

    def test_get_request_gnss_client(self):
        res = self.client().get('/gnss', headers=self.client_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

    def test_patch_request_gnss(self):
        res = self.client().patch('/gnss')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    # -----------------------------------------------------------------------------------------------------------

    def test_get_request_gnss_signals(self):
        res = self.client().get('/gnss-signals')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_get_request_gnss_signals_director(self):
        res = self.client().get('/gnss-signals', headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

    def test_get_request_gnss_signals_client(self):
        res = self.client().get('/gnss-signals', headers=self.client_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

    def test_patch_request_gnss_signals(self):
        res = self.client().patch('/gnss-signals')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    # -----------------------------------------------------------------------------------------------------------

    def test_post_gnss(self):
        res = self.client().post('/gnss',
                                 json={'name': 'Beidou', 'owner': 'China', 'num_satellites': 35, 'num_frequencies': 5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_post_gnss_director(self):
        res = self.client().post('/gnss', headers=self.director_auth_header,
                                 json={'name': 'Beidou', 'owner': 'China', 'num_satellites': 35, 'num_frequencies': 5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

    def test_post_gnss_client(self):
        res = self.client().post('/gnss', headers=self.client_auth_header,
                                 json={'name': 'Beidou', 'owner': 'China', 'num_satellites': 35, 'num_frequencies': 5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_post_gnss_400(self):
        res = self.client().post('/gnss', headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_post_gnss_405(self):
        res = self.client().patch('/gnss',
                                  json={'name': 'Beidou', 'owner': 'China', 'num_satellites': 35, 'num_frequencies': 5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    # -----------------------------------------------------------------------------------------------------------

    def test_post_gnss_signals(self):
        res = self.client().post('/gnss-signals',
                                 json={'signal': 'B1', 'gnss_id': 2})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_post_gnss_signals_director(self):
        res = self.client().post('/gnss-signals', headers=self.director_auth_header,
                                 json={'signal': 'B1', 'gnss_id': 2})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

    def test_post_gnss_signals_client(self):
        res = self.client().post('/gnss-signals', headers=self.client_auth_header,
                                 json={'signal': 'B1', 'gnss_id': 2})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_post_gnss_signals_400(self):
        res = self.client().post('/gnss-signals', headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_post_gnss_signals_405(self):
        res = self.client().patch('/gnss-signals',
                                  json={'signal': 'B1', 'gnss_id': 2})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    # -----------------------------------------------------------------------------------------------------------

    def test_patch_gnss(self):
        res = self.client().patch('/gnss/1', json={'owner': 'America'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_patch_gnss_director(self):
        res = self.client().patch('/gnss/1', headers=self.director_auth_header,
                                  json={'owner': 'America'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

    def test_patch_gnss_client(self):
        res = self.client().patch('/gnss/1', headers=self.client_auth_header,
                                  json={'owner': 'America'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_patch_gnss_400(self):
        res = self.client().patch('/gnss/1', headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_patch_gnss_404(self):
        res = self.client().patch('/gnss/3', headers=self.director_auth_header,
                                  json={'owner': 'America'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_patch_gnss_405(self):
        res = self.client().get('/gnss/1', json={'owner': 'America'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    # -----------------------------------------------------------------------------------------------------------

    def test_patch_gnss_signal(self):
        res = self.client().patch('/gnss-signals/1', json={'signal': 'F1'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_patch_gnss_signal_director(self):
        res = self.client().patch('/gnss-signals/1',
                                  headers=self.director_auth_header, json={'signal': 'F1'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

    def test_patch_gnss_signal_client(self):
        res = self.client().patch('/gnss-signals/1',
                                  headers=self.client_auth_header, json={'signal': 'F1'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_patch_gnss_signal_400(self):
        res = self.client().patch('/gnss-signals/1', headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_patch_gnss_signal_404(self):
        res = self.client().patch('/gnss-signals/10',
                                  headers=self.director_auth_header, json={'signal': 'F1'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_patch_gnss_signal_405(self):
        res = self.client().get('/gnss-signals/1', json={'signal': 'F1'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    # -----------------------------------------------------------------------------------------------------------

    def test_delete_gnss(self):
        res = self.client().delete('/gnss/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_delete_gnss_director(self):
        res = self.client().delete('/gnss/1', headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)
        self.assertTrue(len(data))

    def test_delete_gnss_client(self):
        res = self.client().delete('/gnss/1', headers=self.client_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_delete_gnss_404(self):
        res = self.client().delete('/gnss/3', headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_delete_gnss_405(self):
        res = self.client().get('/gnss/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    # -----------------------------------------------------------------------------------------------------------

    def test_delete_gnss_signals(self):
        res = self.client().delete('/gnss-signals/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_delete_gnss_signals_director(self):
        res = self.client().delete('/gnss-signals/1', headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)
        self.assertTrue(len(data))

    def test_delete_gnss_signals_client(self):
        res = self.client().delete('/gnss-signals/1', headers=self.client_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_delete_gnss_signals_404(self):
        res = self.client().delete('/gnss-signals/10', headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    def test_delete_gnss_signals_405(self):
        res = self.client().get('/gnss-signals/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(data))

    # -----------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()
