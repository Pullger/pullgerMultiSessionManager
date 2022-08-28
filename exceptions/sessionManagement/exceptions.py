from ..exceptions import General as RootGeneral

class General(RootGeneral):
    def __init__(self, message, **kwargs):
        from pullgerMultisessionManager import updateLoggerNameInKWARGS
        updateLoggerNameInKWARGS('SessionManager', kwargs)
        super().__init__(message, **kwargs)

class Execute(General):
    def __init__(self, message, **kwargs):
        from pullgerMultisessionManager import updateLoggerNameInKWARGS
        updateLoggerNameInKWARGS('Execute', kwargs)
        super().__init__(message, **kwargs)

class ConnectionInitialization(General):
    def __init__(self, message, **kwargs):
        from pullgerMultisessionManager import updateLoggerNameInKWARGS
        updateLoggerNameInKWARGS('ConnectionInitialization', kwargs)
        super().__init__(message, **kwargs)

class SqirrelOperation(General):
    def __init__(self, message, **kwargs):
        from pullgerMultisessionManager import updateLoggerNameInKWARGS
        updateLoggerNameInKWARGS('SqirrelOperation', kwargs)
        super().__init__(message, **kwargs)

class DomainOperation(General):
    def __init__(self, message, **kwargs):
        from pullgerMultisessionManager import updateLoggerNameInKWARGS
        updateLoggerNameInKWARGS('DomainOperation', kwargs)
        super().__init__(message, **kwargs)
