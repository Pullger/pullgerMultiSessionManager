import uuid
from django.apps import apps
from pullgerInternalControl.pullgerMultiSessionManager.API import exceptions


def add_task(**kwargs):
    msm_app = apps.get_app_config('pullgerMultiSessionManager')
    uuid_task = msm_app.multi_session_manager.taskStack.add_task(**kwargs)
    if 'taskProcessor' in kwargs:
        try:
            kwargs['taskProcessor'].setSendedStatus()
            msm_app.multisessionManager.taskStack.allow_execution_task(uuid_task)
        except BaseException as e:
            msm_app.multi_session_manager.taskStack.delete_task(uuid_task)


def add_sync_task(task_for_processing):
    msm_app = apps.get_app_config('pullgerMultiSessionManager')
    return msm_app.multi_session_manager.add_sync_task(task_for_processing)


def execute_task_in_the_queue(*args, **kwargs):
    msm_app = apps.get_app_config('pullgerMultiSessionManager')
    return msm_app.multi_session_manager.task_execute(*args, **kwargs)


def execute_finalizer(*args, **kwargs):
    msm_app = apps.get_app_config('pullgerMultiSessionManager')
    msm_app.multi_session_manager.tasks_finalize()


def add_new_session(authorization=None, conn=None, **kwargs):
    """
    Creating new operation session

    :param authorization: CLASS of subclass pullgerAccountManager.authorizationsServers : authorization server
    :param conn:
    :param kwargs:
    :return:
    """
    from pullgerAccountManager import authorizationsServers
    from pullgerSquirrel import connectors

    msm_app = apps.get_app_config('pullgerMultiSessionManager')

    session_params = {
        'authorization': None,
        'conn': None
    }

    if conn is not None:
        if isinstance(conn, str):
            session_params['conn'] = connectors.get_by_name(conn)
        else:
            session_params['conn'] = conn

    if authorization is not None:
        if type(authorization) == str:
            session_params['authorization'] = authorizationsServers.getByName(authorization)
        else:
            session_params['authorization'] = authorization

    return msm_app.multi_session_manager.sessionManager.add_new_session(**session_params)


def kill_session(uuid_session=None, session=None, **kwargs):
    msm_app = apps.get_app_config('pullgerMultiSessionManager')

    if uuid_session is not None or session is not None:
        return msm_app.multi_session_manager.sessionManager.kill_session(uuid_session=uuid_session, session=session)
    else:
        exceptions.General(
            msg="Incorrect send data",
            level=40
        )


def get_sessions_list():
    msm_app = apps.get_app_config('pullgerMultiSessionManager')
    return msm_app.multi_session_manager.sessionManager.get_session_list()


def get_session_by_uuid(uuid_session):
    msm_app = apps.get_app_config('pullgerMultiSessionManager')
    return msm_app.multi_session_manager.sessionManager.get_session_by_uuid(uuid_session)


def make_all_session_authorization():
    msm_app = apps.get_app_config('pullgerMultiSessionManager')
    msm_app.multi_session_manager.sessionManager.make_all_authorization()


def operation_get_page(uuid_session: str = None, url: str = None, **kwargs):
    msm_app = apps.get_app_config('pullgerMultiSessionManager')
    if uuid_session is not None:
        msm_app.multi_session_manager.operationExecutor.get_page(uuid_session=uuid_session, url=url)
    else:
        raise exceptions.General(msg=f"Incorrect uuid_session : [{uuid_session}]")


def operation_get_html(uuid_session: str = None, **kwargs):
    msm_app = apps.get_app_config('pullgerMultiSessionManager')
    if (uuid_session is not None) and (len(uuid_session) == 36):
        return msm_app.multi_session_manager.operationExecutor.get_html(uuid_session=uuid_session)
    else:
        raise exceptions.General(msg=f"Incorrect uuid_session : [{uuid_session}]")


def operation_get_current_url(uuid_session: str = None, **kwargs):
    msm_app = apps.get_app_config('pullgerMultiSessionManager')
    if (uuid_session is not None) and (len(uuid_session) == 36):
        return msm_app.multi_session_manager.operationExecutor.get_current_url(uuid_session=uuid_session)
    else:
        raise exceptions.General(msg=f"Incorrect uuid_session : [{uuid_session}]")


def operation_elements_scan(uuid_session: str = None):
    msm_app = apps.get_app_config('pullgerMultiSessionManager')
    if uuid_session is not None:
        return msm_app.multi_session_manager.operationExecutor.elements_scan(uuid_session=uuid_session)
    else:
        raise exceptions.General(msg=f"Incorrect uuid_session : [{uuid_session}]")


def operation_elements_list(uuid_session: str = None):
    msm_app = apps.get_app_config('pullgerMultiSessionManager')
    if uuid_session is not None:
        try:
            return msm_app.multi_session_manager.operationExecutor.elements_list(uuid_session=uuid_session)
        except BaseException as e:
            raise exceptions.General(
                exception=e
            )
    else:
        raise exceptions.General(
            msg=f"Incorrect uuid_session : [{uuid_session}]",
            level=30
        )


def operation_element_send_string(uuid_session: str, uuid_auto_element: str, string: str):
    msm_app = apps.get_app_config('pullgerMultiSessionManager')
    if uuid_session is not None:
        try:
            return msm_app.multi_session_manager.operationExecutor.element_send_string(
                uuid_session=uuid_session,
                uuid_auto_element=uuid_auto_element,
                string=string
            )
        except BaseException as e:
            raise exceptions.General(
                exception=e
            )
    else:
        raise exceptions.General(
            msg=f"Incorrect uuid_session : [{uuid_session}]",
            level=30
        )


def operation_send_enter(uuid_session: str):
    msm_app = apps.get_app_config('pullgerMultiSessionManager')
    if uuid_session is not None:
        try:
            return msm_app.multi_session_manager.operationExecutor.send_enter(
                uuid_session=uuid_session
            )
        except BaseException as e:
            raise exceptions.General(
                exception=e
            )
    else:
        raise exceptions.General(
            msg=f"Incorrect uuid_session : [{uuid_session}]",
            level=30
        )


def operation_element_send_enter(uuid_session: str, uuid_auto_element: str):
    msm_app = apps.get_app_config('pullgerMultiSessionManager')
    if uuid_session is not None:
        try:
            return msm_app.multi_session_manager.operationExecutor.element_send_enter(
                uuid_session=uuid_session,
                uuid_auto_element=uuid_auto_element
            )
        except BaseException as e:
            raise exceptions.General(
                exception=e
            )
    else:
        raise exceptions.General(
            msg=f"Incorrect uuid_session : [{uuid_session}]",
            level=30
        )


def operation_element_click(uuid_session: str, uuid_auto_element: str):
    msm_app = apps.get_app_config('pullgerMultiSessionManager')
    if uuid_session is not None:
        try:
            return msm_app.multi_session_manager.operationExecutor.element_click(
                uuid_session=uuid_session,
                uuid_auto_element=uuid_auto_element
            )
        except BaseException as e:
            raise exceptions.General(
                exception=e
            )
    else:
        raise exceptions.General(
            msg=f"Incorrect uuid_session : [{uuid_session}]",
            level=30
        )
