import uuid

import pullgerSquirrel
from pullgerInternalControl import pIC_pMSM
from pullgerInternalControl import pIC_pD


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
        __slots__ = '_connectionManager'

        def __init__(self, cm, **kwargs):
            self._connectionManager = cm

        def get_page(self, uuid_session: str, url: str, **kwargs):
            session = self._connectionManager.sessionManager.get_session_by_uuid(uuid_session=uuid_session)
            session.squirrel.get_page(url)

        def get_html(self, uuid_session: str, **kwargs):
            session = self._connectionManager.sessionManager.get_session_by_uuid(uuid_session=uuid_session)
            return session.squirrel.get_html()

        def get_current_url(self, uuid_session: str, **kwargs):
            session = self._connectionManager.sessionManager.get_session_by_uuid(uuid_session=uuid_session)
            return session.squirrel.current_url

        def elements_scan(self, uuid_session: str, **kwargs):
            session = self._connectionManager.sessionManager.get_session_by_uuid(uuid_session=uuid_session)
            if session is not None:
                return session.squirrel.elements_scan()
            else:
                raise pIC_pMSM.SessionManagement.General(
                    msg=f'Session with uuid [{uuid_session}] not found.',
                    level=30
                )

        def elements_list(self, uuid_session: str, **kwargs):
            session = self._connectionManager.sessionManager.get_session_by_uuid(uuid_session=uuid_session)
            if session is not None:
                return session.squirrel.elements_list()
            else:
                raise pIC_pMSM.SessionManagement.General(
                    msg=f'Session with uuid [{uuid_session}] not found.',
                    level=30
                )

        def element_send_string(self, uuid_session: str, uuid_auto_element: str, string: str):
            session = self._connectionManager.sessionManager.get_session_by_uuid(uuid_session=uuid_session)
            if session is not None:
                web_elem = session.squirrel.elements_get(uuid_auto_element=uuid_auto_element)
                web_elem.send_string(string=string)
            else:
                raise pIC_pMSM.SessionManagement.General(
                    msg=f'Session with uuid [{uuid_session}] not found.',
                    level=30
                )

        def element_send_enter(self, uuid_session: str, uuid_auto_element: str):
            session = self._connectionManager.sessionManager.get_session_by_uuid(uuid_session=uuid_session)
            if session is not None:
                web_elem = session.squirrel.elements_get(uuid_auto_element=uuid_auto_element)
                web_elem.send_enter()
            else:
                raise pIC_pMSM.SessionManagement.General(
                    msg=f'Session with uuid [{uuid_session}] not found.',
                    level=30
                )

        def send_enter(self, uuid_session: str):
            session = self._connectionManager.sessionManager.get_session_by_uuid(uuid_session=uuid_session)
            if session is not None:
                session.squirrel.send_enter()
            else:
                raise pIC_pMSM.SessionManagement.General(
                    msg=f'Session with uuid [{uuid_session}] not found.',
                    level=30
                )

        def element_click(self, uuid_session: str, uuid_auto_element: str):
            session = self._connectionManager.sessionManager.get_session_by_uuid(uuid_session=uuid_session)
            if session is not None:
                web_elem = session.squirrel.elements_get(uuid_auto_element=uuid_auto_element)
                web_elem.click()
            else:
                raise pIC_pMSM.SessionManagement.General(
                    msg=f'Session with uuid [{uuid_session}] not found.',
                    level=30
                )



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

        def delete_task(self, uuid_task: str = None):
            if uuid_task is not None \
                    and isinstance(uuid_task, str) \
                    and len(uuid_task) == 36:

                found = False
                for index, curTask in enumerate(self._taskList):
                    if curTask['uuid'] == uuid_task:
                        del self._taskList[index]
                        found = True
                        break

                if found is not True:
                    raise pIC_pMSM.TaskStack.General(
                        msg=f'Cant delete task with uuid: [{uuid_task}]: Task not found.',
                        level=40
                    )
            else:
                raise pIC_pMSM.TaskStack.TypeCheckError(
                    msg=f'Cant delete task with uuid: [{uuid_task}]. Incorrect value.',
                    level=40
                )

        def allow_execution_task(self, uuid_task: str = None):
            if uuid_task is not None \
                    and isinstance(uuid_task, str) \
                    and len(uuid_task) == 36:

                found = False
                for curTask in self._taskList:
                    if curTask['uuid'] == uuid_task:
                        self._setExecutePermissionToTask(curTask, True)
                        found = True
                        break

                if found is not True:
                    raise pIC_pMSM.TaskStack.General(
                        msg=f'Cant set to allow task with uuid {uuid_task}: task not found',
                        level=30
                    )
            else:
                raise pIC_pMSM.TaskStack.TypeCheckError(
                    msg=f'Cant delete task with uuid: [{uuid_task}]. Incorrect value.',
                    level=40
                )

        def get_next_operation(self):
            if len(self._taskList) != 0:
                return self._taskList.pop(0)
            else:
                return None

    class SessionManagerClass(object):
        __slots__ = '_sessionsList'

        def __init__(self):
            self._sessionsList = []

        class SessionClass(object):
            __slots__ = ('uuid_session', 'connector', 'squirrel', 'domain',
                         'account', 'authorization', 'active', 'in_use',
                         'initialized', 'ready', 'live')

            def __init__(self, uuid_session: str = None, connector=None, squirrel=None, domain=None,
                         account=None, authorization=None, active: bool = True, in_use: bool = False,
                         initialized: bool = False, ready: bool = False, live: bool = False):
                self.uuid_session = uuid_session
                self.connector = connector
                self.squirrel = squirrel
                self.domain = domain
                self.account = account
                self.authorization = authorization
                self.active = active
                self.in_use = in_use
                self.initialized = initialized
                self.ready = ready
                self.live = live

            @property
            def structure(self):
                return {
                    'uuid': str(self.uuid_session),
                    'uuid_session': str(self.uuid_session),
                    'connector': self.connector,
                    'authorization': self.authorization,
                    'used_account': False if self.account is None else True,
                    'active': self.active,
                    'in_use': self.in_use,
                    'ready': self.ready,
                    'live': self.live,
                }

        # @staticmethod
        # def session_structure(**kwargs):
        #     return {
        #         'uuid': str(kwargs['uuid']) if 'uuid' in kwargs else None,
        #         'connector': kwargs['connector'] if 'connector' in kwargs else None,
        #         'squirrel': kwargs['squirrel'] if 'squirrel' in kwargs else None,
        #         'domain': kwargs['domain'] if 'domain' in kwargs else None,
        #         'account': kwargs['account'] if 'account' in kwargs else None,
        #         'authorization': kwargs['authorization'] if 'authorization' in kwargs else None,
        #         'active': kwargs['active'] if 'active' in kwargs else True,  # Permission to use session
        #         'inUse': kwargs['inUse'] if 'inUse' in kwargs else False,  # Flag using session
        #         'initialized': kwargs['initialized'] if 'initialized' in kwargs else False,
        #         'ready': kwargs['ready'] if 'ready' in kwargs else False,
        #         'live': kwargs['live'] if 'live' in kwargs else False,
        #     }

        def operation_structure(self):
            return {
                'operation': None,
                'executing': False,
            }

        def get_session_list(self):
            listOfSessions = []
            for cur_session in self._sessionsList:
                listOfSessions.append(cur_session.structure)
                # {
                #     'uuid': str(cur_session['uuid']),
                #     'connector': cur_session['connector'],
                #     'authorization': cur_session['authorization'],
                #     'usedAccount': False if cur_session['account'] is None else True,
                #     'active': cur_session['active'],
                #     'inUse': cur_session['inUse'],
                #     'ready': cur_session['ready'],
                #     'live': cur_session['live'],
                # }
                # )
            return listOfSessions

        def get_session_by_uuid(self, uuid_session: str):
            for cur_session in self._sessionsList:
                if cur_session.uuid_session == uuid_session:
                    return cur_session
            return None

        def generate_session_package(self, authorizationServer=None, authorizationType=None, MaxAmount=None):
            if MaxAmount is not None:
                for countSession in range(MaxAmount):
                    self.add_new_session()

        def execute_regulations_session_operations(self):
            """
            Key procedure for periodic reglament operation with sessions
            """
            self.close_disabled_sessions()
            self.delete_disabled_sessions()

        def deleteSessionFromList(self, uuid):
            for cur_session in self._sessionsList:
                if cur_session.uuid_session == uuid:
                    if cur_session.active is False \
                            and cur_session.squirrel is None \
                            and cur_session.in_use is False:
                        del self._sessionsList[self._sessionsList.index(cur_session)]
                        return True
                    break
            return False

        def close_disabled_session(self, uuid_session):
            try:
                for cur_session in self._sessionsList:
                    if cur_session.uuid_session == uuid_session:
                        if cur_session.active is False:
                            if cur_session.in_use is False:
                                if cur_session.squirrel is not None:
                                    try:
                                        cur_session.squirrel.close()
                                        cur_session.squirrel = None
                                        return True
                                    except BaseException as e:
                                        raise pIC_pMSM.SessionManagement.SqirrelOperation(
                                            'Error on closing session',
                                            level=50,
                                            exception=e
                                        )
                                elif cur_session.domain is not None:
                                    try:
                                        cur_session.domain.close()
                                        cur_session.domain = None
                                        return True
                                    except BaseException as e:
                                        raise pIC_pMSM.SessionManagement.DomainOperation(
                                            'Error on closing domain',
                                            level=50,
                                            exception=e
                                        )
                        break
            except:
                pass

            return False

        def close_disabled_sessions(self):
            for cur_session in self._sessionsList:
                self.close_disabled_session(cur_session.uuid_session)

        def delete_disabled_sessions(self):
            """
            Delete all session from list if they not in use
            """

            sessionForDelete = []
            for cur_session in self._sessionsList:
                sessionForDelete.append()

            for cur_session_for_delete in sessionForDelete:
                self._deleteSessionFromList(cur_session_for_delete)

        def disable_all_sessions(self):
            for cur_session in self._sessionsList:
                self.disable_session(cur_session.uuid_session)

        def disable_session(self, uuid_session: str):
            for cur_session in self._sessionsList:
                if cur_session.uuid_session == uuid_session:
                    cur_session.active = False
                    return True
            return False

        def kill_session(self, uuid_session: str, **kwargs):
            if self.disable_session(uuid_session):
                if self.close_disabled_session(uuid_session):
                    if self.deleteSessionFromList(uuid_session):
                        return True;
            return False

        def add_new_session(self, authorization=None, conn=None, **kwargs):
            # =================================================================
            squirrel = pullgerSquirrel.Squirrel(conn=conn)
            squirrel.initialize()
            if authorization is None:
                try:
                    uuid_session = str(uuid.uuid4())
                    self._sessionsList.append(
                        self.SessionClass(
                            uuid_session=uuid_session,
                            connector=conn,
                            squirrel=squirrel,
                            live=True,
                            initialized=True,
                        )
                    )
                    return uuid_session
                except BaseException as e:
                    raise pIC_pMSM.SessionManagement.ConnectionInitialization(
                        msg="Critical error on initialisation. Internal description.",
                        level=50,
                        exception=e
                    )
            else:
                domainClass = authorization.getDomain()
                domain = domainClass(squirrel)

                if domain.initialized is True:
                    uuid_session = str(uuid.uuid4())
                    self._sessionsList.append(
                        self.SessionClass(
                            uuid_session=uuid_session,
                            connector=conn,
                            authorization=authorization,
                            squirrel=squirrel,
                            domain=domain,
                            live=True
                        )
                    )
                    return uuid_session
                else:
                    raise pIC_pMSM.SessionManagement.ConnectionInitialization(
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
                    if cur_session.account == curAccount:
                        accountUse = True
                        break

                if accountUse is True:
                    break

                for cur_session in self._sessionsList:
                    if cur_session.authorization is not None and cur_session.account is None:
                        try:
                            cur_session.account = curAccount
                            cur_session.domain.authorization(cur_session.account.login,
                                                             pAM__API.decripteMessage(cur_session.account.password))
                            cur_session.ready = True
                        except BaseException as e:
                            cur_session.account = None
                            cur_session.ready = False

                            raise pIC_pMSM.SessionManagement.MakeAuthorization(
                                'Unexpected initialize domain status',
                                level=50,
                                exception=e
                            )

        def get_free_session(self, authorization=None):
            for cur_session in self._sessionsList:
                if authorization is not None:
                    if str(cur_session.authorization) != str(authorization):
                        continue
                if cur_session.active is not True \
                        and cur_session.in_use is not True \
                        and cur_session.live is not True:
                    continue

                self.session_domain_put_in_use_true(cur_session.uuid_session)
                return cur_session.uuid_session
            return None

        def session_domain_get(self, uuid_session):
            for cur_session in self._sessionsList:
                if cur_session.uuid_session is uuid_session:
                    return cur_session.domain

            raise pIC_pMSM.General(
                msg=f"Can't find session with UUID {uuid_session}",
                level=40
            )

        def session_domain_put_in_use_true(self, uuid_session):
            for findSession in self._sessionsList:
                if findSession.uuid_session is uuid_session:
                    findSession.in_use = True
                    return

            raise pIC_pMSM.SessionManagement.General(
                msg=f"Can't find session with UUID {uuid_session}",
                level=40
            )

        def session_domain_set_in_use_false(self, uuid_session: str):
            for findSession in self._sessionsList:
                if findSession.uuid_session is uuid_session:
                    findSession.in_use = False
                    return

            raise pIC_pMSM.SessionManagement.General(
                msg=f"Can't find session with UUID {uuid_session}",
                level=40
            )

        def execute_operation_on_free_session(self, operation):
            uuid_session = self.get_free_session(operation['authorization'])
            if uuid_session is not None:
                try:
                    operation['loader'].executeOnDomain(self.session_domain_get(uuid_session))

                except pIC_pD.General as e:
                    raise pIC_pMSM.SessionManagement.Execute(
                        msg=f"Error on executing task",
                        level=40,
                        exception=e
                    )
                except BaseException as e:
                    raise pIC_pMSM.SessionManagement.Execute(
                        msg=f"Error on executing task",
                        level=40,
                        exception=e
                    )
                finally:
                    self.session_domain_set_in_use_false(uuid_session)

    class TaskFinishedStack(object):
        __slots__ = '_taskFinishedStack'

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

        def add_error_operation(self, operation, error):
            sentStructure = operation.copy()
            sentStructure['status_code'] = 400
            sentStructure['status_discription'] = str(error)

            self._taskFinishedStack.append(self.finisherStructure(**sentStructure))

        def add_finish_operation(self, operation):
            self._taskFinishedStack.append(self.finisherStructure(**operation))

    def task_execute(self):
        returnStatus = False
        operation = self.taskStack.get_next_operation()
        if operation is not None:
            try:
                self.sessionManager.execute_operation_on_free_session(operation)
                self.taskFinishedStack.add_finish_operation(operation)
                returnStatus = True
            except BaseException as e:
                self.taskFinishedStack.add_error_operation(operation, e)
        return returnStatus

    def tasks_finalize(self):
        is_end = False
        indexList = 0
        while is_end is False:
            if len(self.taskFinishedStack._taskFinishedStack) - 1 >= indexList:
                curFinTask = self.taskFinishedStack._taskFinishedStack[indexList]
                try:
                    try:
                        self.taskFinishedStack._taskFinishedStack.remove(curFinTask)
                        curFinTask['finalizer']()
                    except BaseException as e:
                        raise pIC_pMSM.TaskFinalization.General('Error on finalisation', level=50, exeptation=e)
                except:
                    indexList += 1
            else:
                is_end = True
