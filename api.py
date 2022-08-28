from django.apps import apps

def addTask(**kwargs):
    reglament_app = apps.get_app_config('pullgerMultisessionManager')
    uuid_task = reglament_app.multisessionManager.taskStack.addTask(**kwargs)
    if 'taskProcessor' in kwargs:
        try:
            kwargs['taskProcessor'].setSendedStatus()
            reglament_app.multisessionManager.taskStack.allowExecutionTask(uuid_task)
        except BaseException as e:
            reglament_app.multisessionManager.taskStack.deleteTask(uuid_task)

def executeTask():
    reglament_app = apps.get_app_config('pullgerMultisessionManager')
    reglament_app.multisessionManager.taskExecute()

def executeFinalizer():
    reglament_app = apps.get_app_config('pullgerMultisessionManager')
    reglament_app.multisessionManager.tasksFinalize()

def addNewSession(**kwargs):
    '''
    Creating new operation session

    :param kwargs:
        authorization: CLASS of subclass pullgerAccountManager.authorizationsServers : authorization server
        authorizationRootServerName: STRING: name of root authorization server
    :return:
    '''
    from pullgerAccountManager import structures

    reglament_app = apps.get_app_config('pullgerMultisessionManager')
    # return reglament_app.multisessionManager.sessionManager.addNewSession(authorization=structures.authorizationsServers.linkedin())
    if 'authorization' in kwargs:
        return reglament_app.multisessionManager.sessionManager.addNewSession(authorization=kwargs['authorization'])
    elif 'authorizationRootServerName' in kwargs:
        return reglament_app.multisessionManager.sessionManager.addNewSession(authorization=structures.authorizationsServers.getByNames(kwargs['authorizationRootServerName']))
    else:
        return reglament_app.multisessionManager.sessionManager.addNewSession()

def killSession(**kwargs):
    reglament_app = apps.get_app_config('pullgerMultisessionManager')
    if 'uuid' in kwargs:
        result = reglament_app.multisessionManager.sessionManager.killSession(kwargs['uuid'])
    else:
        result = False

    return result

def getSessionsList():
    reglament_app = apps.get_app_config('pullgerMultisessionManager')
    return reglament_app.multisessionManager.sessionManager.getSessionList()

def makeAllSessionAutorization():
    reglament_app = apps.get_app_config('pullgerMultisessionManager')
    reglament_app.multisessionManager.sessionManager.makeAllAutorization()
