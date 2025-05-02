import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()

def addLoggingLevel(levelName, levelNum, methodName=None):
    if not methodName:
        methodName = levelName.lower()
    
    if hasattr(logging, levelName) or hasattr(logging, methodName) or hasattr(logging.getLoggerClass(), methodName):
        return
    
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)
    
    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)
    
    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)

def setup_logging():
    try:
        addLoggingLevel('RESULT', 35)
    except AttributeError:
        pass
    
    log_type = os.getenv('BROWSER_USE_LOGGING_LEVEL', 'info').lower()
    log_file = os.getenv('BROWSER_USE_LOGGING_FILE', 'browser_use.log')

    if logging.getLogger().hasHandlers():
        return
    
    root = logging.getLogger()
    root.handlers = []
    
    class BrowserUseFormatter(logging.Formatter):
        def format(self, record):
            if isinstance(record.name, str) and record.name.startswith('browser_use.'):
                record.name = record.name.split('.')[-2]
            return super().format(record)
    
    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')  # 'w' mode clears previous logs
    
    formatter = BrowserUseFormatter('%(levelname)-8s [%(name)s] %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    if log_type == 'result':
        console_handler.setLevel('RESULT')
        file_handler.setLevel('RESULT')
    elif log_type == 'debug':
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
    
    root.addHandler(console_handler)
    root.addHandler(file_handler)
    
    if log_type == 'result':
        root.setLevel('RESULT')
    elif log_type == 'debug':
        root.setLevel(logging.DEBUG)
    else:
        root.setLevel(logging.INFO)
    
    browser_use_logger = logging.getLogger('browser_use')
    browser_use_logger.propagate = False
    browser_use_logger.addHandler(console_handler)
    browser_use_logger.addHandler(file_handler)
    browser_use_logger.setLevel(root.level)
    
    logger = logging.getLogger('browser_use')
    logger.info('BrowserUse logging setup complete with level %s', log_type)
    
    for logger_name in [
        'WDM', 'httpx', 'selenium', 'playwright', 'urllib3', 'asyncio', 'langchain',
        'openai', 'httpcore', 'charset_normalizer', 'anthropic._base_client',
        'PIL.PngImagePlugin', 'trafilatura.htmlprocessing', 'trafilatura'
    ]:
        third_party = logging.getLogger(logger_name)
        third_party.setLevel(logging.ERROR)
        third_party.propagate = False
