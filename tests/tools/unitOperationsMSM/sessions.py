from django.test import TestCase
from pullgerMultiSessionManager import apiMSM
from pullgerSquirrel.connectors.selenium import connector
from pullgerSquirrel.SquirrelCore import Session


def kill_session(self: TestCase, session: Session):
    result_kill_session = apiMSM.kill_session(session=session)
    self.assertEqual(result_kill_session, True, 'Error on killing session')


def add_new_linkedin_session(self: TestCase):
    try:
        new_session = apiMSM.add_new_session(conn=connector.chrome.standard, authorization='linkedin.general')
    except BaseException as e:
        self.assertNotEqual(True, False, f"Error on creating new session. Description: {str(e)}")
    else:
        self.assertIsInstance(new_session, Session, "Incorrect return on create new session.")
        return new_session


def add_new_session_selenium_standard(self):
    session = apiMSM.add_new_session(conn=connector.chrome.standard)
    self.assertNotEqual(session, None, 'Error on creating new session')
    return session


def add_new_session_selenium_headless(self):
    session_uuid = apiMSM.add_new_session(conn=connector.chrome.headless)
    self.assertNotEqual(session_uuid, None, 'Error on creating new session')

    return session_uuid


def add_new_session_selenium_stand_alone(self):
    session_uuid = apiMSM.add_new_session(conn=connector.stand_alone.general)
    self.assertNotEqual(session_uuid, None, 'Error on creating new session')

    return session_uuid
