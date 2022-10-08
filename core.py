import uuid
import pullgerSquirrel
from pullgerExceptions import pullgerMultiSessionManager as exceptions
from pullgerExceptions import pullgerDomain as exceptions_pullgerDomain
from pullgerLogin.pullgerMultiSessionManager import logger
LOGGER_NAME = "pullger.MultisessionManager.generator"


class ConnectionManager:
    __slots__ = (
        'taskStack',
        'taskExecutingStack',
        'taskFinishedStack',
        'sessionManager',
        'operationExecutor'
    )

    def __init__(self):
        self.taskStack = self.TaskStackClass()
        self.taskFinishedStack = self.TaskFinishedStack()
        self.sessionManager = self.SessionManagerClass()
        self.operationExecutor = self.OperationExecutorClass(cm=self)

    class OperationExecutorClass:
        __slots__ = 'connectionManager'

        def __init__(self, cm, **kwargs):
            self.connectionManager = cm

        def get_page(self, uuid_session: str, url: str, **kwargs):
            session = self.connectionManager.sessionManager.get_session_by_uuid(uuid_session=uuid_session)
            session['squirrel'].get_page(url)

        def get_html(self, uuid_session: str, **kwargs):
            session = self.connectionManager.sessionManager.get_session_by_uuid(uuid_session=uuid_session)
            return session['squirrel'].get_html()


    class TaskStackClass(object):
        __slots__ = "_taskList"

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

        def add_task(self, **kwargs):
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
                raise exceptions.TaskStack.General(f'Cant delete task with uuid {uuid}: task not found')

        def allowExecutionTask(self, uuid):
            finded = False
            for curTask in self._taskList:
                if curTask['uuid'] == uuid:
                    self._setExecutePermissionToTask(curTask, True)
                    finded = True
                    break

            if finded == True:
                return True
            else:
                raise exceptions.TaskStack.General(f'Cant set to allow task with uuid {uuid}: task not found')

        def getNextOperation(self):
            if len(self._taskList) != 0:
                return self._taskList.pop(0)
            else:
                return None

    class SessionManagerClass(object):
        __slots__ = '_sessionsList'

        def __init__(self):
            self._sessionsList = []

        @staticmethod
        def session_structure(**kwargs):
            return {
                'uuid': str(kwargs['uuid']) if 'uuid' in kwargs else None,
                'connector': kwargs['connector'] if 'connector' in kwargs else None,
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

        def get_session_list(self):
            listOfSessions = []
            for cur_session in self._sessionsList:
                listOfSessions.append(
                    {
                        'uuid': str(cur_session['uuid']),
                        'connector': cur_session['connector'],
                        'authorization': cur_session['authorization'],
                        'usedAccount': False if cur_session['account'] is None else True,
                        'active': cur_session['active'],
                        'inUse': cur_session['inUse'],
                        'ready': cur_session['ready'],
                        'live': cur_session['live'],
                    }
                )
            return listOfSessions

        def get_session_by_uuid(self, uuid_session: str):
            for cur_session in self._sessionsList:
                if cur_session['uuid'] == uuid_session:
                    return cur_session
            return None

        def generateSessinPackage(self, authorizationServer=None, authorizationType=None, MaxAmount=None):
            if MaxAmount != None:
                for countSession in range(MaxAmount):
                    self.add_new_session()

        def executeReglamentSessionOperations(self):
            '''
            Key procedure for periodic reglament operation with sessions
            '''
            self.closeDisabledSessions()
            self.deleteDisabledSessions()

        def deleteSessionFromList(self, uuid):
            for cur_session in self._sessionsList:
                if cur_session['uuid'] == uuid:
                    if cur_session['active'] == False and cur_session['squirrel'] is None and cur_session['inUse'] == False:
                        del self._sessionsList[self._sessionsList.index(cur_session)]
                        return True;
                    break
            return False

        def closeDisabledSession(self, uuid):
            try:
                for cur_session in self._sessionsList:
                    if cur_session['uuid'] == uuid:
                        if cur_session['active'] == False:
                            if cur_session['inUse'] == False:
                                if cur_session['squirrel'] != None:
                                    try:
                                        cur_session['squirrel'].close()
                                        cur_session['squirrel'] = None
                                        return True
                                    except BaseException as e:
                                        raise exceptions.SessionManagement.SqirrelOperation(
                                            'Error on closing session',
                                            level=50,
                                            exception=e
                                        )
                                elif cur_session['domain'] != None:
                                    try:
                                        cur_session['domain'].close()
                                        cur_session['domain'] = None
                                        return True
                                    except BaseException as e:
                                        raise exceptions.SessionManagement.DomainOperation(
                                            'Error on closing domain',
                                            level=50,
                                            exception=e
                                        )
                        break
            except:
                pass

            return False

        def closeDisabledSessions(self):
            for cur_session in self._sessionsList:
                self.closeDisabledSession(cur_session['uuid'])

        def deleteDisabledSessions(self):
            '''
            Delete all session from list if they not in use
            '''

            sessionForDelete = []
            for cur_session in self._sessionsList:
                sessionForDelete.append()

            for cur_session_for_delete in sessionForDelete:
                self._deleteSessionFromList(cur_session_for_delete)

        def disableAllSessions(self):
            for cur_session in self._sessionsList:
                self.disableSession(cur_session['uuid'])

        def disableSession(self, uuid):
            for cur_session in self._sessionsList:
                if cur_session['uuid'] == uuid:
                    cur_session['active'] = False
                    return True
            return False

        def kill_session(self, uuid: str, **kwargs):
            if self.disableSession(uuid):
                if self.closeDisabledSession(uuid):
                    if self.deleteSessionFromList(uuid):
                        return True;
            return False

        def add_new_session(self, authorization=None, conn=None, **kwargs):
            # =================================================================
            logger.debug(f"add_new_session start")
            squirrel = pullgerSquirrel.Squirrel(conn=conn)
            squirrel.initialize()
            if authorization is None:
                try:
                    uuidSession = str(uuid.uuid4())
                    self._sessionsList.append(
                        self.session_structure(
                            uuid=uuidSession,
                            connector=conn,
                            squirrel=squirrel,
                            live=True,
                            initialized=True,
                        )
                    )
                    return uuidSession
                except BaseException as e:
                    raise exceptions.SessionManagement.ConnectionInitialization(
                        msg="Critical error on initialisation. Internal description.",
                        level=50,
                        exception=e
                    )
            else:
                domainClass = authorization.getDomain()
                domain = domainClass(squirrel)

                if domain.initialized is True:
                    uuidSession = str(uuid.uuid4())
                    self._sessionsList.append(
                        self.session_structure(
                            uuid=uuidSession,
                            connector=conn,
                            authorization=authorization,
                            squirrel=squirrel,
                            domain=domain,
                            live=True
                        )
                    )
                    return uuidSession
                else:
                    raise exceptions.SessionManagement.ConnectionInitialization(
                        'Unexpected initialize domain status',
                        level=50
                    )

        def makeAllAutorization(self):
            from pullgerAccountManager.models import Accounts
            from pullgerAccountManager import api as pAM__API

            allAccounts = list(Accounts.objects.getActualList())

            for curAccount in allAccounts:
                accountUse = False
                for cur_session in self._sessionsList:
                    if cur_session['account'] == curAccount:
                        accountUse = True
                        break

                if accountUse is True:
                    break

                for cur_session in self._sessionsList:
                    if cur_session['authorization'] is not None and cur_session['account'] is None:
                        try:
                            cur_session['account'] = curAccount
                            cur_session['domain'].authorization(cur_session['account'].login, pAM__API.decripteMessage(cur_session['account'].password))
                            cur_session['ready'] = True
                        except BaseException as e:
                            cur_session['account'] = None
                            cur_session['ready'] = False

                            raise exceptions.SessionManagement.MakeAuthorization(
                                'Unexpected initialize domain status',
                                level=50,
                                exception=e
                            )

        def GetFreeSession(self, inAuthorization = None):
            for cur_session in self._sessionsList:
                if inAuthorization != None:
                    if str(cur_session['authorization']) != str(inAuthorization):
                        continue
                if cur_session['active'] != True and cur_session['inUse'] != True and cur_session['live'] != True:
                    continue

                self.SessionDomainPUT_INUSE_TRUE(cur_session['uuid'])
                return cur_session['uuid']
            return None

        def SessionDomainGET(self, inUUID):
            for testSession in self._sessionsList:
                if testSession['uuid'] == inUUID:
                    return testSession['domain']
            raise exceptions.SessionManagement.General(f"Can't find session with UUID {inUUID}", loggerName=LOGGER_NAME, level=40)

        def SessionDomainPUT_INUSE_TRUE(self, inUUID):
            for findSession in self._sessionsList:
                if findSession['uuid'] == inUUID:
                    findSession['inUse'] = True
                    return
            raise exceptions.SessionManagement.General(f"Can't find session with UUID {inUUID}", loggerName=LOGGER_NAME, level=40)

        def SessionDomainSET_INUSE_FALSE(self, inUUID):
            for findSession in self._sessionsList:
                if findSession['uuid'] == inUUID:
                    findSession['inUse'] = False
                    return
            raise exceptions.SessionManagement.General(f"Can't find session with UUID {inUUID}", loggerName=LOGGER_NAME, level=40)

        def ExecuteOperationOnFreeSession(self, inOperation):
            sessionUUID = self.GetFreeSession(inOperation['authorization'])
            if sessionUUID is not None:
                try:
                    inOperation['loader'].executeOnDomain(self.SessionDomainGET(sessionUUID))
                except exceptions_pullgerDomain.General as e:
                    raise exceptions.SessionManagement.Execute(
                        f"Error on executing task", loggerName=LOGGER_NAME, level=40, exception=e)
                except BaseException as e:
                    raise exceptions.SessionManagement.Execute(f"Error on executing task", loggerName=LOGGER_NAME, level=40, exception=e)
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

    def task_execute(self):
        returnStatus = False
        operation = self.taskStack.getNextOperation()
        if operation != None:
            try:
                self.sessionManager.ExecuteOperationOnFreeSession(operation)
                self.taskFinishedStack.addFinishOperation(operation)
                returnStatus = True
            except BaseException as e:
                self.taskFinishedStack.addErrorOperation(operation, e)
        return returnStatus

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
                        raise exceptions.TaskFinalization.General('Error on finalisation', level=50, exeptation=e)
                except:
                    indexList += 1
            else:
                isEnd = True
        pass