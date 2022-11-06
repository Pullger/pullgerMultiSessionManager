from django.test import TestCase
from django.apps import apps
from pullgerMultiSessionManager import apiMSM, core
from ..tools import unitOperationsMSM


class Test000API(TestCase):
    def test_001_00_00_SessionManager_smoke(self):
        def create_and_kill_standard_sessions():
            session_uuid = unitOperationsMSM.add_new_session_general_no_head()

            resultKillSession = apiMSM.kill_session(uuid_session=session_uuid)
            self.assertEqual(resultKillSession, None, 'Error on killing empy session')

        def create_and_kill_authorization_linkedin_sessions():
            uuid_session = unitOperationsMSM.add_new_linkedin_session()
            unitOperationsMSM.kill_session(uuid_session)

        create_and_kill_standard_sessions()
        create_and_kill_authorization_linkedin_sessions()

    def test_000_00_00_SessionManager_getSessionList(self):
        test_uuid = [apiMSM.add_new_session(), apiMSM.add_new_session()]
        sessionList = apiMSM.get_sessions_list()

        for index in range(0, 2):
            self.assertEqual(sessionList[index]['uuid'], test_uuid[index])
