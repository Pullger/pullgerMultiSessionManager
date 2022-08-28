import uuid
import pullgerSquirrel as squirrel
# from pullgerSquirrel import exceptions as exceptationsPullgerSquirrel
from pullgerMultisessionManager import exceptions

LOGGER_NAME = "pullger.MultisessionManager.generator"

class ConnectionManager():
    __slots__ = (
        'taskStack',
        'taskExecutingStack',
        'taskFinishedStack',
        'sessionManager'
    )

    def __init__(self):
        self.taskStack = self.TaskStackClass()
        self.taskFinishedStack = self.TaskFinishedStack()
        self.sessionManager = self.SessionManagerClass()

    class TaskStackClass(object):
        __slots__ = ('_taskList')

        def __init__(self):
            self._taskList = []

        @staticmethod
        def __getStructure(**kwargs):
            return {
                'uuid': kwargs['uuid'] if 'uuid' in kwargs else None,
                'execute_permission': kwargs['execute_permission'] if 'execute_permission' in kwargs else False,
                'authorization': kwargs['authorization'] if 'authorization' in kwargs else None,
                'loader': kwargs['loader'] if 'loader' in kwargs else None,
                'finalizer': kwargs['finalizer'] if 'finalizer' in kwargs else None,
            }

        def addTask(self, **kwargs):
            newTaskStructure = self.__getStructure(
                uuid=str(uuid.uuid4()),
                authorization=kwargs['authorization'] if 'authorization' in kwargs else None,
                loader=kwargs['loader'] if 'loader' in kwargs else None,
                finalizer=kwargs['taskFinalizer'] if 'taskFinalizer' in kwargs else None,
            )
            self._taskList.append(newTaskStructure)
            return newTaskStructure['uuid']

        @staticmethod
        def _setExecutePermissionToTask(task, newStatus):
            task['execute_permission'] = newStatus

        def deleteTask(self, uuid):
            finded = False
            for index, curTask  in enumerate(self._taskList):
                if curTask['uuid'] == uuid:
                    del self._taskList[index]
                    finded = True;
                    break

            if finded == True:
                return True
            else:
                raise exceptions.taskStack.General(f'Cant delete task with uuid {uuid}: task not found')

        def allowExecutionTask(self, uuid):
            finded = False
            for curTask in self._taskList:
                if curTask['uuid'] == uuid:
                    self._setExecutePermissionToTask(curTask, True)
                    finded = True;
                    break

            if finded == True:
                return True
            else:
                raise exceptions.taskStack.General(f'Cant set to allow task with uuid {uuid}: task not found')

        def getNextOperation(self):
            if len(self._taskList) != 0:
                return self._taskList.pop(0)
            else:
                return None

    class SessionManagerClass(object):
        __slots__ = ('_sessionsList')

        def __init__(self):
            self._sessionsList = []

        def sessionStructure(self, **kwargs):
            return {
                'uuid': str(kwargs['uuid']) if 'uuid' in kwargs else None,
                'squirrel': kwargs['squirrel'] if 'squirrel' in kwargs else None,
                'domain': kwargs['domain'] if 'domain' in kwargs else None,
                'account': kwargs['account'] if 'account' in kwargs else None,
                'authorization': kwargs['authorization'] if 'authorization' in kwargs else None,
                'active': kwargs['active'] if 'active' in kwargs else True,  # Permission to use session
                'inUse': kwargs['inUse'] if 'inUse' in kwargs else False,  # Flag using session
                'initialized': kwargs['initialized'] if 'initialized' in kwargs else False,
                'ready': kwargs['ready'] if 'ready' in kwargs else False,
                'live': kwargs['live'] if 'live' in kwargs else False,
            }

        def operationStructure(self):
            return {
                'operation': None,
                'executing': False,
            }

        def generateConnections(self, inService):
            pass

        def distributedRun(self):
            pass

        def getSessionList(self):
            listOfSessions = []
            for curSession in self._sessionsList:
                listOfSessions.append(
                    {
                        'uuid': str(curSession['uuid']),
                        'authorization': curSession['authorization'],
                        'usedAccount': False if curSession['account'] == None else True,
                        'active': curSession['active'],
                        'inUse': curSession['inUse'],
                        'ready': curSession['ready'],
                        'live': curSession['live'],
                    }
                )
            return listOfSessions

        def generateSessinPackage(self, authorizationServer=None, authorizationType=None, MaxAmount=None):
            if MaxAmount != None:
                for countSession in range(MaxAmount):
                    self.addNewSession()

        def executeReglamentSessionOperations(self):
            '''
            Key procedure for periodic reglament operation with sessions
            '''
            self.closeDisabledSessions()
            self.deleteDisabledSessions()

        def deleteSessionFromList(self, uuid):
            for curSession in self._sessionsList:
                if curSession['uuid'] == uuid:
                    if curSession['active'] == False and curSession['squirrel'] == None and curSession['inUse'] == False:
                        del self._sessionsList[self._sessionsList.index(curSession)]
                        return True;
                    break
            return False

        def closeDisabledSession(self, uuid):
            try:
                for curSession in self._sessionsList:
                    if curSession['uuid'] == uuid:
                        if curSession['active'] == False:
                            if curSession['inUse'] == False:
                                if curSession['squirrel'] != None:
                                    try:
                                        curSession['squirrel'].close()
                                        curSession['squirrel'] = None
                                        return True
                                    except BaseException as e:
                                        raise exceptions.sessionManagement.SqirrelOperation(
                                            'Error on closing session',
                                            level=50,
                                            exception=e
                                        )
                                elif curSession['domain'] != None:
                                    try:
                                        curSession['domain'].close()
                                        curSession['domain'] = None
                                        return True
                                    except BaseException as e:
                                        raise exceptions.sessionManagement.DomainOperation(
                                            'Error on closing domain',
                                            level=50,
                                            exception=e
                                        )
                        break
            except:
                pass

            return False

        def closeDisabledSessions(self):
            for curSession in self._sessionsList:
                self.closeDisabledSession(curSession['uuid'])

        def deleteDisabledSessions(self):
            '''
            Delete all session from list if they not in use
            '''

            sessionForDelete = []
            for curSession in self._sessionsList:
                sessionForDelete.append()

            for curSessionForDelete in sessionForDelete:
                self._deleteSessionFromList(curSessionForDelete)

        def disableAllSessions(self):
            for curSession in self._sessionsList:
                self.disableSession(curSession['uuid'])

        def disableSession(self, uuid):
            for curSession in self._sessionsList:
                if curSession['uuid'] == uuid:
                    curSession['active'] = False
                    return True
            return False

        def killSession(self, uuid):
            if self.disableSession(uuid):
                if self.closeDisabledSession(uuid):
                    if self.deleteSessionFromList(uuid):
                        return True;
            return False


        def addNewSession(self, **kwargs):
            # =================================================================
            if 'authorization' in kwargs:
                authorization = kwargs['authorization']
            else:
                authorization = None
            # =================================================================

            if authorization == None:
                Squirrel = squirrel.Squirrel(connector=squirrel.Connectors.selenium)
                Squirrel.initialize()

                try:
                    uuidSession = str(uuid.uuid4())
                    self._sessionsList.append(
                        self.sessionStructure(
                            uuid=uuidSession,
                            squirrel=Squirrel,
                            live=True,
                            initialized=True,
                        )
                    )
                    return uuidSession
                except BaseException as e:
                    raise exceptions.sessionManagement.ConnectionInitialization('Critical error on initialisation. Internal discription.', level=50, exception=e)
            else:
                domainClass = authorization.getDomain()

                Squirrel = squirrel.Squirrel(squirrel.Connectors.selenium)
                Squirrel.initialize()
                domain = domainClass(Squirrel)

                if domain.initialized == True:
                    uuidSession = str(uuid.uuid4())
                    self._sessionsList.append(
                        self.sessionStructure(
                            uuid=uuidSession,
                            domain=domain,
                            authorization=authorization,
                            live=True
                        )
                    )
                    return uuidSession
                else:
                    raise exceptions.sessionManagement.ConnectionInitialization(
                        'Unexpected initialize domain status',
                        level=50
                    )

        def makeAllAutorization(self):
            from pullgerAccountManager.models import Accounts

            allAccounts = list(Accounts.objects.getActualList())

            for curAccount in allAccounts:
                accountUse = False
                for curSession in self._sessionsList:
                    if curSession['account'] == curAccount:
                        accountUse = True;
                        break

                if accountUse == True:
                    break

                for curSession in self._sessionsList:
                    if curSession['authorization'] != None and curSession['account'] == None:
                        curSession['account'] = curAccount
                        curSession['domain'].authorization(curSession['account'].login, curSession['account'].password)
                        curSession['ready'] = True

        def GetFreeSession(self, inAuthorization = None):
            for curSession in self._sessionsList:
                if inAuthorization != None:
                    if curSession['authorization'].fullName != inAuthorization.fullName:
                        continue
                if curSession['active'] != True and curSession['inUse'] != True and curSession['live'] != True:
                    continue

                self.SessionDomainPUT_INUSE_TRUE(curSession['uuid'])
                return curSession['uuid']
            return None

        def SessionDomainGET(self, inUUID):
            for testSession in self._sessionsList:
                if testSession['uuid'] == inUUID:
                    return testSession['domain']
            raise exceptions.sessionManagement.General(f"Can't find session with UUID {inUUID}", loggerName=LOGGER_NAME, level=40)

        def SessionDomainPUT_INUSE_TRUE(self, inUUID):
            for findSession in self._sessionsList:
                if findSession['uuid'] == inUUID:
                    findSession['inUse'] = True
                    return
            raise exceptions.sessionManagement.General(f"Can't find session with UUID {inUUID}", loggerName=LOGGER_NAME, level=40)


        def SessionDomainSET_INUSE_FALSE(self, inUUID):
            for findSession in self._sessionsList:
                if findSession['uuid'] == inUUID:
                    findSession['inUse'] = False
                    return
            raise exceptions.sessionManagement.General(f"Can't find session with UUID {inUUID}", loggerName=LOGGER_NAME, level=40)

        def ExecuteOperationOnFreeSession(self, inOperation):
            sessionUUID = self.GetFreeSession(inOperation['authorization'])
            if sessionUUID != None:
                try:
                    inOperation['loader'].executeOnDomain(self.SessionDomainGET(sessionUUID))
                except excDomain as e:
                    raise exceptions.sessionManagement.Execute(
                        f"Error on executing task", loggerName=LOGGER_NAME, level=40, exception=e)
                except BaseException as e:
                    raise exceptions.sessionManagement.Execute(f"Error on executing task", loggerName=LOGGER_NAME, level=40, exception=e)
                finally:
                    self.SessionDomainSET_INUSE_FALSE(sessionUUID)

    class TaskFinishedStack(object):
        __slots__ = ('_taskFinishedStack')

        def __init__(self):
            self._taskFinishedStack = []

        def finisherStructure(self, **kwargs):
            return {
                'uuid': str(kwargs['uuid']) if 'uuid' in kwargs else None,
                'uuid_link': str(kwargs['uuid_link']) if 'uuid_link' in kwargs else None,
                'finalizer': kwargs['finalizer'] if 'finalizer' in kwargs else None,
                'status_code': kwargs['status_code'] if 'status_code' in kwargs else 200,
                'status_discription': kwargs['status_discription'] if 'status_discription' in kwargs else None,
            }

        def addErrorOperation(self, inOperation, error):
            sentStructure = inOperation.copy()
            sentStructure['status_code'] = 400
            sentStructure['status_discription'] = str(error)

            self._taskFinishedStack.append(self.finisherStructure(**sentStructure))

        def addFinishOperation(self, inOperation):
            self._taskFinishedStack.append(self.finisherStructure(**inOperation))

    def taskExecute(self):
        operation = self.taskStack.getNextOperation()
        if operation != None:
            try:
                raise BaseException("Exception")
                self.sessionManager.ExecuteOperationOnFreeSession(operation)
                self.taskFinishedStack.addFinishOperation(operation)
            except BaseException as e:
                self.taskFinishedStack.addErrorOperation(operation, e)

    def tasksFinalize(self):
        isEnd = False
        indexList = 0
        while isEnd == False:
            if len(self.taskFinishedStack._taskFinishedStack)-1 >= indexList:
                curFinTask = self.taskFinishedStack._taskFinishedStack[indexList]
                try:
                    try:
                        self.taskFinishedStack._taskFinishedStack.remove(curFinTask)
                        curFinTask['finalizer']()
                    except BaseException as e:
                        raise exceptions.taskFinalization.General('Error on finalisation', level=50, exeptation=e)
                except:
                    indexList += 1
            else:
                isEnd = True
        pass