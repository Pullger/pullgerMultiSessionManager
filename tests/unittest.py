from django.test import TestCase
from django.apps import apps
from pullgerMultisessionManager_1 import api, core


class Test_000_API(TestCase):
    def test_001_SessionManager_smoke(self):
        def createAndKillStandardSessions():
            sessionUUID = api.addNewSession()
            self.assertNotEqual(sessionUUID, None, 'Error on creating new session')
            resultKillSession = api.killSession(uuid=sessionUUID)
            self.assertEqual(resultKillSession, None, 'Error on killing empy session')
        def createAndKillAuthorizationLinkedINSessions():
            sessionUUID = api.addNewSession(authorizationRootServerName='linkedin')
            self.assertNotEqual(sessionUUID, None, 'Error on creating new session')
            resultKillSession = api.killSession(uuid=sessionUUID)
            self.assertEqual(resultKillSession, None, 'Error on killing empy session')

        createAndKillStandardSessions();
        createAndKillAuthorizationLinkedINSessions()

    def test_000_SessionManager_getSessionList(self):
        testUUID = []
        testUUID.append(api.addNewSession())
        testUUID.append(api.addNewSession())
        sessionList = api.getSessionsList()

        for index in range(0, 2):
            self.assertEqual(sessionList[index]['uuid'] , testUUID[index])

class Test_001_Operation(TestCase):
    def test_001_initiation(self):
        '''
            Testing mechenisme initialisation
        '''


        reglament_app = apps.get_app_config('pullgerMultisessionManager')
        self.assertIsInstance(reglament_app.multisessionManager, core.ConnectionManager, " Incorrect creating on django APP")

    def test_002_TaskStack(self):
        reglament_app = apps.get_app_config('pullgerMultisessionManager')
        multisessionManager = reglament_app.multisessionManager

        def smokeTest():
            uuidTask1 = None
            uuidTask2 = None

            def addTask():

                global uuidTask1
                uuidTask1 = multisessionManager.taskStack.addTask()
                self.assertIsInstance(uuidTask1, str, 'Incorrect retyrn type')
                self.assertEqual(len(uuidTask1), 36, 'Incorrect retyrn type')

                self.assertEqual(len(multisessionManager.taskStack._taskList), 1, "Incorrect append task")
                self.assertEqual(multisessionManager.taskStack._taskList[0]['uuid'], uuidTask1, "Incorrect task creating")

                global uuidTask2
                uuidTask2 = multisessionManager.taskStack.addTask()
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

            uuidTask1 = multisessionManager.taskStack.addTask(**taskStructure1)
            for curTSkey,  curTSValue in taskStructure1.items():
                self.assertIn(curTSkey, multisessionManager.taskStack._taskList[0], "Property does't exist.")
                self.assertEqual(multisessionManager.taskStack._taskList[0][curTSkey], curTSValue, 'Incorrect data translation.')
            multisessionManager.taskStack.deleteTask(uuidTask1)

        # def exceptations():
        #     multisessionManager.taskStack.deleteTask('sfsfsf')
        #     pass

        smokeTest()
        internalIntegration()

    def test_003_SessionManager(self):
        reglament_app = apps.get_app_config('pullgerMultisessionManager')
        multisessionManager = reglament_app.multisessionManager

        def smokeTest():
            sessionUUID = multisessionManager.sessionManager.addNewSession()
            killResult =  multisessionManager.sessionManager.killSession(sessionUUID)
            self.assertEqual(killResult, True, "Can't kill session after creation.")

        smokeTest()