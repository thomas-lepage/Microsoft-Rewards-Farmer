from enum import Enum
import logging
import os

class LogColor(Enum):
    RED = 1
    GREEN = 2
    PURPLE = 3
    YELLOW = 4

class Logger:
    def __init__(self):
        logging.TRACE = 51
        logging.addLevelName(logging.TRACE, "TRACE")

        def _trace(logger, message, *args, **kwargs):
            if logger.isEnabledFor(logging.TRACE):
                logger._log(logging.TRACE, message, args, **kwargs)

        logging.Logger.trace = _trace 

        #now we will Create and configure logger 
        logPath = os.path.dirname(os.path.abspath(__file__)) + '/ms-rewards.log'
        logging.basicConfig(filename=logPath, 
                            format='%(asctime)s %(message)s', 
                            filemode='a+') 
        #Let us Create an object 
        self.logger = logging.getLogger() 
        self.logger.setLevel(logging.TRACE)

    def log(self, module, text, color=None):
        '''
        Log text (can be multiline) under the given module.
        E.g. log('[FOO]', 'Hello\nWorld') will log:
        [FOO] Hello
        [FOO] World
        Optionally use a color (used only in console, not in the actual log file).
        '''
        log_lines = '\n'.join([module + ' ' + x for x in text.splitlines()])
        self.logger.trace(log_lines)
        if color is None:
            print(log_lines)
        else:
            color_code = {LogColor.RED: '\033[31m', \
                LogColor.GREEN: '\033[32m', \
                LogColor.PURPLE: '\033[35m', \
                LogColor.YELLOW: '\033[33m', \
            }[color]
            print("{0}{1}\033[00m".format(color_code, log_lines))
