from ..exceptions import General as RootGeneral

class General(RootGeneral):
    def __init__(self, message, **kwargs):
        from pullgerMultisessionManager import updateLoggerNameInKWARGS
        updateLoggerNameInKWARGS('TaskStack', kwargs)
        super().__init__(message, **kwargs)

class SystemError(General):
    def __init__(self, message, **kwargs):
        from pullgerMultisessionManager import updateLoggerNameInKWARGS
        updateLoggerNameInKWARGS('SystemError', kwargs)
        super().__init__(message, **kwargs)