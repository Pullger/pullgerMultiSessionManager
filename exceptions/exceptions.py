class General(BaseException):
    def __init__(self, message, **kwargs):
        super().__init__(message)
        # Logger initialization
        import logging
        from pullgerMultisessionManager import updateLoggerNameInKWARGS
        updateLoggerNameInKWARGS('pullgerMultisessionManager', kwargs)

        logger = logging.getLogger(kwargs['loggerName'])

        # Write internal error discription
        if 'exception' in kwargs:
            logMessage = f"{message} Internal discription: [{str(kwargs['exception'])}]"
        else:
            logMessage = message
        # Logger level
        if 'level' in kwargs and type(kwargs['level']) == int:
            logger.log(kwargs['level'], logMessage)
        else:
            logger.critical(logMessage)

class ConnectionInitialization(General):
    def __init__(self, message, **kwargs):
        from pullgerMultisessionManager import updateLoggerNameInKWARGS
        updateLoggerNameInKWARGS('ConnectionInitialization', kwargs)
        super().__init__(message, **kwargs)

class SessionManagement(General):
    def __init__(self, message, **kwargs):
        from pullgerMultisessionManager import updateLoggerNameInKWARGS
        updateLoggerNameInKWARGS('SessionManagement', kwargs)
        super().__init__(message, **kwargs)