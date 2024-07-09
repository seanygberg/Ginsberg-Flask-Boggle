from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client:
            res = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('high_score'))
            self.assertIsNone(session.get('times_played'))

    def test_valid_word(self):
        """Test if word is valid"""

        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = client.post('/check-word', data={'word': 'cat'})
        self.assertEqual(response.json['result'], 'ok')
        
    def test_valid_word_not_on_board(self):
        """Test if word is valid, but not on the board"""

        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = client.post('/check-word', data={'word': 'Aaron'})
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_invalid_word(self):
        """Test if word is invalid"""

        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = client.post('/check-word', data={'word': 'CAT'})
        self.assertEqual(response.json['result'], 'not-word')
        
if __name__ == '__main__': 
    unittest.main() 