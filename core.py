import uuid as uuid_class
import importlib

import pullgerSquirrel
from pullgerInternalControl import pIC_pMSM
from pullgerInternalControl import pIC_pD
from pullgerInternalControl import pIC_pS

from pullgerDataSynchronization import commonDS


def get_function_by_name(model_class, name):
    return getattr(model_class, name)


class ConnectionManager:
    __slots__ = (
        '_task_stack',
        '_task_finished_stack',
        'sessionManager',
        'operationExecutor'
    )

    def __del_(self):
        pass

    def __init__(self):
        self._task_stack = self.TaskStackClass(connection_manager=self)
        self._task_finished_stack = self.TaskFinishedStack()
        self.sessionManager = self.SessionManagerClass()
        self.operationExecutor = self.OperationExecutorClass(connection_manager=self)
        from pullgerDataSynchronization import models
        models.ExecutionStackLinks.objects.initialization_clear()

    class OperationExecutorClass:
        __slots__ = '_connectionManager'

        def __init__(self, connection_manager, **kwargs):
            self._connectionManager = connection_manager

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
        __slots__ = ("_task_list", "_connection_manager")

        def __init__(self, connection_manager):
            self._task_list = []
            self._connection_manager = connection_manager

        class MultiSessionTask:
            __slots__ = (
                'uuid_ms_task',
                'uuid_sync_task',
                'uuid_element',
                'handle',
                'table',
                'model',
                'execute_permission',
                'authorization',
                'connectors',
                'status_code',
                'status_description',
                '_connection_manager'
            )

            def __del__(self):
                pass

            def __init__(
                    self,
                    uuid_sync_task: str = None,
                    uuid_element: str = None,
                    handle: str = None,
                    model=None,
                    authorization=None,
                    connectors=None,
                    connection_manager=None
            ):
                self.uuid_ms_task = uuid_class.uuid4()
                self.uuid_element = uuid_element
                self.uuid_sync_task = uuid_sync_task
                self.handle = handle
                self.model = model
                self.execute_permission = False
                self.authorization = authorization
                self.connectors = connectors
                self.status_code = None
                self.status_description = ''
                self._connection_manager = connection_manager

            def _set_success(self):
                self.status_code = 200
                self.status_description = None

            def _set_error(self, error_code: int, error_description: str):
                self.status_code = error_code
                self.status_description = error_description

            def finalize(self):
                from pullgerDataSynchronization.models import ExecutionStackLinks

                ExecutionStackLinks.finalize(
                    uuid=self.uuid_sync_task,
                    status_code=self.status_code,
                    status_description=self.status_description
                )

                self._connection_manager._task_finished_stack._task_finished_list.remove(self)

            def return_to_queue(self):
                self._connection_manager._task_stack.return_task_to_queue(self)

            def set_executed(self, error=None, error_code=500):
                if error is None:
                    self._set_success()
                else:
                    self._set_error(error_code=error_code, error_description=str(error))
                self._connection_manager._task_finished_stack._task_finished_list.append(self)

        def add_task(self, **kwargs):
            new_task_structure = self.__getStructure(
                uuid=str(uuid_class.uuid4()),
                authorization=kwargs['authorization'] if 'authorization' in kwargs else None,
                loader=kwargs['loader'] if 'loader' in kwargs else None,
                finalizer=kwargs['taskFinalizer'] if 'taskFinalizer' in kwargs else None,
            )
            self._task_list.append(new_task_structure)
            return new_task_structure['uuid']

        def add_task_in_list(self, task):
            self._task_list.append(task)

        def return_task_to_queue(self, task):
            self._task_list.insert(0, task)

        def delete_task(self, uuid_task: str = None):
            if uuid_task is not None \
                    and isinstance(uuid_task, str) \
                    and len(uuid_task) == 36:

                found = False
                for index, curTask in enumerate(self._task_list):
                    if curTask['uuid'] == uuid_task:
                        del self._task_list[index]
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
                for curTask in self._task_list:
                    if curTask['uuid'] == uuid_task:
                        self._set_execute_permission_to_task(curTask, True)
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

        def get_next_task(self):
            if len(self._task_list) != 0:
                return self._task_list.pop(0)
            else:
                return None

        @staticmethod
        def _set_execute_permission_to_task(task, newStatus):
            task.execute_permission = newStatus

    class SessionManagerClass(object):
        __slots__ = '_sessions_list'

        def __init__(self):
            self._sessions_list = []

        def __del__(self):
            pass

        @staticmethod
        def operation_structure():
            return {
                'operation': None,
                'executing': False,
            }

        def get_session_list(self):
            list_of_sessions = []
            for cur_session in self._sessions_list:
                list_of_sessions.append(cur_session.structure)
            return list_of_sessions

        def get_session_by_uuid(self, uuid_session: str):
            for cur_session in self._sessions_list:
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

        def delete_session_from_list(self, uuid):
            for cur_session in self._sessions_list:
                if cur_session.uuid_session == uuid:
                    if cur_session.active is False \
                            and cur_session.squirrel is None \
                            and cur_session.in_use is False:
                        del self._sessions_list[self._sessions_list.index(cur_session)]
                        return True
                    break
            return False

        @staticmethod
        def close_disabled_session(session):
            if session.active is False:
                if session.in_use is False:
                    if session.squirrel is not None:
                        try:
                            session.squirrel.close()
                            return True
                        except BaseException as e:
                            raise pIC_pMSM.SessionManagement.SqirrelOperation(
                                'Error on closing session',
                                level=50,
                                exception=e
                            )
                        finally:
                            session.squirrel = None
                    elif session.domain is not None:
                        try:
                            session.domain.close()
                            return True
                        except BaseException as e:
                            raise pIC_pMSM.SessionManagement.DomainOperation(
                                'Error on closing domain',
                                level=50,
                                exception=e
                            )
                        finally:
                            session.domain = None
            return True

        def close_disabled_sessions(self):
            for cur_session in self._sessions_list:
                self.close_disabled_session(cur_session.uuid_session)

        def delete_disabled_sessions(self):
            """
            Delete all session from list if they not in use
            """

            session_for_delete = []
            for cur_session in self._sessions_list:
                session_for_delete.append(cur_session)

            for cur_session_for_delete in session_for_delete:
                self._deleteSessionFromList(cur_session_for_delete)

        def disable_all_sessions(self):
            for cur_session in self._sessions_list:
                self.disable_session(cur_session.uuid_session)

        @staticmethod
        def disable_session(session: str):
            session.active = False
            return True

        def kill_session(self, uuid_session: str = None, session=None, **kwargs):
            if uuid_session is not None:
                session = self.get_session_by_uuid(uuid_session)

            if self.disable_session(session):
                if self.close_disabled_session(session):
                    if self.delete_session_from_list(str(session)):
                        return True
            return False

        def add_new_session(self, authorization=None, conn=None, **kwargs):
            new_session = pullgerSquirrel.Session(conn=conn, authorization=authorization)
            self._sessions_list.append(new_session)

            return new_session

        def make_all_authorization(self):
            from pullgerAccountManager.models import Accounts
            from pullgerAccountManager import apiAM

            all_accounts = list(Accounts.objects.getActualList())

            for curAccount in all_accounts:
                account_use = False
                for cur_session in self._sessions_list:
                    if cur_session.account == curAccount:
                        account_use = True
                        break

                if account_use is True:
                    break

                for cur_session in self._sessions_list:
                    if cur_session.authorization is not None and cur_session.account is None:
                        try:
                            cur_session.account = curAccount
                            cur_session.domain.authorization(
                                cur_session.account.login,
                                apiAM.decrypt_message(cur_session.account.password)
                            )
                            cur_session.ready = True
                        except BaseException as e:
                            cur_session.account = None
                            cur_session.ready = False

                            raise pIC_pMSM.SessionManagement.MakeAuthorization(
                                'Unexpected initialize domain status',
                                level=50,
                                exception=e
                            )

        def get_free_session(self, authorization=None, connectors=None):
            for cur_session in self._sessions_list:
                if str(cur_session.authorization) not in authorization:
                    continue
                if str(cur_session.connector) not in connectors:
                    continue

                if cur_session.active is not True \
                        or cur_session.in_use is True \
                        or cur_session.live is not True:
                    continue

                self.session_domain_put_in_use_true(cur_session.uuid_session)
                return cur_session
            return None

        def session_domain_get(self, uuid_session):
            for cur_session in self._sessions_list:
                if cur_session.uuid_session is uuid_session:
                    return cur_session.domain

            raise pIC_pMSM.General(
                msg=f"Can't find session with UUID {uuid_session}",
                level=40
            )

        def session_domain_put_in_use_true(self, uuid_session):
            for findSession in self._sessions_list:
                if findSession.uuid_session is uuid_session:
                    findSession.in_use = True
                    return

            raise pIC_pMSM.SessionManagement.General(
                msg=f"Can't find session with UUID {uuid_session}",
                level=40
            )

        @staticmethod
        def session_set_available(session: str):
            session.in_use = False

        def execute_operation_on_free_session(self, multy_session_task):
            result = False

            session = self.get_free_session(multy_session_task.authorization, multy_session_task.connectors)
            if session is not None:
                try:
                    model_class = commonDS.get_model_class_by_name(multy_session_task.model)
                    synced_elem = model_class.objects.get_by_uuid(uuid=multy_session_task.uuid_element)

                    executor = get_function_by_name(synced_elem, multy_session_task.handle)
                    executor(session=session)

                except pIC_pD.General as e:
                    raise pIC_pD.General(
                        msg=f"Error loading domain: [{str(e)}]",
                        level=40,
                        exception=e
                    )
                except BaseException as e:
                    raise pIC_pMSM.SessionManagement.Execute(
                        msg=f"Error on executing task: [{str(e)}]",
                        level=40,
                        exception=e
                    )
                else:
                    result = True
                finally:
                    self.session_set_available(session=session)
            else:
                result = None

            return result

    class TaskFinishedStack(object):
        __slots__ = '_task_finished_list'

        def __init__(self):
            self._task_finished_list = []

        def __del__(self):
            pass

    def task_execute(self, *args, **kwargs):
        return_status = None
        task = self._task_stack.get_next_task()
        try:
            if task is not None:
                result_execution = self.sessionManager.execute_operation_on_free_session(task)
                if result_execution is True:
                    task.set_executed()
                    return_status = True
                    print(f"TASK {str(task.uuid_ms_task)}: successfully executed.")
                elif result_execution is None:
                    task.return_to_queue()
                    print(f"TASK {str(task.uuid_ms_task)}: not executed. (no task to execute)")
            else:
                print(f"No TASK found in queue.")
        except pIC_pS.ErrorOnLoadPage as e:
            task.set_executed(error_code=400, error=e)
            return_status = False
            print(f"Error on executed TASK: {str(task.uuid_ms_task)}. Description: {str(e)}")
        except BaseException as e:
            task.set_executed(error_code=500, error=e)
            return_status = False
            print(f"Error on executed TASK: {str(task.uuid_ms_task)}. Description: {str(e)}")
        return return_status

    def tasks_finalize(self):
        is_end = False
        index_list = 0
        finalized = 0
        finalization_errors = 0
        amount = len(self._task_finished_stack._task_finished_list)
        while is_end is False:
            if len(self._task_finished_stack._task_finished_list) - 1 >= index_list:
                cur_finalize_task = self._task_finished_stack._task_finished_list[index_list]
                try:
                    try:
                        cur_finalize_task.finalize()
                        finalized += 1
                    except BaseException as e:
                        raise pIC_pMSM.TaskFinalization.General('Error on finalisation', level=50, exeptation=e)
                        finalization_errors += 1
                except:
                    index_list += 1
            else:
                is_end = True
        respond = {
            "amount": amount,
            "finalized": finalized,
            "finalization_errors": finalization_errors
        }

        return respond

    def add_sync_task(self, task_for_processing, *args, **kwargs):
        model_class = commonDS.get_model_class_by_name(task_for_processing.model)

        new_multy_session_task = self._task_stack.MultiSessionTask(
            uuid_sync_task=task_for_processing.uuid,
            uuid_element=task_for_processing.uuid_link,
            handle='sync',
            model=task_for_processing.model,
            authorization=model_class.domain.required_authorization_servers_options(),
            connectors=model_class.domain.required_connector_options(),
            connection_manager=self
        )

        self._task_stack.add_task_in_list(new_multy_session_task)
        task_for_processing.set_sent()
        return new_multy_session_task
