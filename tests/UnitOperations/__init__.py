from pullgerMultiSessionManager import api, core
from pullgerSquirrel.connectors.selenium import connector


def kill_session(self, uuid_session: str):
    resultKillSession = api.kill_session(uuid=uuid_session)
    self.assertEqual(resultKillSession, True, 'Error on killing session')

def add_new_linkedin_session(self):
    sessionUUID = api.add_new_session(authorization='linkedin.general')
    self.assertNotEqual(sessionUUID, None, 'Error on creating new session')


def add_new_session_selenium_standard(self):
    session_uuid = api.add_new_session(conn=connector.chrome.standard)
    self.assertNotEqual(session_uuid, None, 'Error on creating new session')

    return session_uuid


def add_new_session_selenium_headless(self):
    session_uuid = api.add_new_session(conn=connector.chrome.headless)
    self.assertNotEqual(session_uuid, None, 'Error on creating new session')

    return session_uuid