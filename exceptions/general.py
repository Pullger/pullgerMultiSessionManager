def updateLoggerNameInKWARGS(loggerName, kwargs):
    '''
    Add upper logger name in dict

    :param loggerName: STRING: name of logger in tree
    :param kwargs: DICT: Arguments list
    :return: No return
    '''
    if 'loggerName' in kwargs:
        kwargs['loggerName'] = loggerName + '.' + kwargs['loggerName']
    else:
        kwargs['loggerName'] = loggerName
