from django.test import TestCase
from django.apps import apps
from pullgerMultiSessionManager import api, core
from . import UnitOperations

class Test_000_00_00_API(TestCase):
    def test_001_00_00_SessionManager_smoke(self):
        def create_and_kill_standard_sessions():
            session_uuid = UnitOperations.add_new_session_general_no_head()

            resultKillSession = api.kill_session(uuid=session_uuid)
            self.assertEqual(resultKillSession, None, 'Error on killing empy session')

        def create_and_kill_authorization_linkedin_sessions():
            uuid_session = UnitOperations.add_new_linkedin_session()
            UnitOperations.kill_session(uuid_session)

        create_and_kill_standard_sessions()
        create_and_kill_authorization_linkedin_sessions()

    def test_000_00_00_SessionManager_getSessionList(self):
        testUUID = []
        testUUID.append(api.add_new_session())
        testUUID.append(api.add_new_session())
        sessionList = api.get_sessions_list()

        for index in range(0, 2):
            self.assertEqual(sessionList[index]['uuid'] , testUUID[index])

class Test_001_00_00_Operation(TestCase):
    def test_001_00_00_initiation(self):
        '''
            Testing mechenisme initialisation
        '''


        reglament_app = apps.get_app_config('pullgerMultiSessionManager')
        self.assertIsInstance(reglament_app.multisessionManager, core.ConnectionManager, " Incorrect creating on django APP")

    def test_002_00_00_TaskStack(self):
        reglament_app = apps.get_app_config('pullgerMultiSessionManager')
        multisessionManager = reglament_app.multisessionManager

        def smokeTest():
            uuidTask1 = None
            uuidTask2 = None

            def addTask():

                global uuidTask1
                uuidTask1 = multisessionManager.taskStack.add_task()
                self.assertIsInstance(uuidTask1, str, 'Incorrect retyrn type')
                self.assertEqual(len(uuidTask1), 36, 'Incorrect retyrn type')

                self.assertEqual(len(multisessionManager.taskStack._taskList), 1, "Incorrect append task")
                self.assertEqual(multisessionManager.taskStack._taskList[0]['uuid'], uuidTask1, "Incorrect task creating")

                global uuidTask2
                uuidTask2 = multisessionManager.taskStack.add_task()
                self.assertIsInstance(uuidTask2, str, 'Incorrect retyrn type')
                self.assertEqual(len(uuidTask2), 36, 'Incorrect retyrn type')

                self.assertEqual(len(multisessionManager.taskStack._taskList), 2, "Incorrect append task")
                self.assertEqual(multisessionManager.taskStack._taskList[1]['uuid'], uuidTask2, "Incorrect task creating")

                self.assertNotEqual(uuidTask1, uuidTask2)

            def deleteTask():
                global uuidTask1
                global uuidTask2

                self.assertEqual(len(multisessionManager.taskStack._taskList), 2, "Incorrect start position")
                multisessionManager.taskStack.deleteTask(uuidTask1)
                self.assertEqual(len(multisessionManager.taskStack._taskList), 1, "Incorrect delete task")
                multisessionManager.taskStack.deleteTask(uuidTask2)
                self.assertEqual(len(multisessionManager.taskStack._taskList), 0, "Incorrect delete task")

            addTask()
            deleteTask()

        def internalIntegration():
            self.assertEqual(len(multisessionManager.taskStack._taskList), 0, "Incorrect initialisation state")

            taskStructure1 = {
                'authorization': 'ATest1',
                'loader': 'LTest1',
                'finisher': 'FTest1',
            }

            uuidTask1 = multisessionManager.taskStack.add_task(**taskStructure1)
            for curTSkey,  curTSValue in taskStructure1.items():
                self.assertIn(curTSkey, multisessionManager.taskStack._taskList[0], "Property does't exist.")
                self.assertEqual(multisessionManager.taskStack._taskList[0][curTSkey], curTSValue, 'Incorrect data translation.')
            multisessionManager.taskStack.deleteTask(uuidTask1)

        # def exceptations():
        #     multisessionManager.taskStack.deleteTask('sfsfsf')
        #     pass

        smokeTest()
        internalIntegration()

    def test_003_00_00_SessionManager(self):
        msm_app = apps.get_app_config('pullgerMultiSessionManager')
        multi_session_manager = msm_app.multi_session_manager

        def smokeTest():
            sessionUUID = multi_session_manager.sessionManager.add_new_session()
            killResult = multi_session_manager.sessionManager.kill_session(sessionUUID)
            self.assertEqual(killResult, True, "Can't kill session after creation.")

        smokeTest()