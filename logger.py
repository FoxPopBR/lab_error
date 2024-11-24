import logging
from logging.handlers import RotatingFileHandler
import os
from functools import wraps
import traceback
import sys

class CustomLogger:
    def __init__(self, name='FoxCoffe', log_file='logError.log', level=logging.INFO, console_log=True, file_log=True, logger_filename='logger.py', include_logger_in_traceback=False):
        self.log_file = os.path.join(os.getcwd(), log_file)
        self.logger = logging.getLogger(name)
        self.level = level
        self.logger_filename = logger_filename
        self.include_logger_in_traceback = include_logger_in_traceback
        self.logger.setLevel(self.level)  # Ensure the logger level is set
        # Prevent adding multiple handlers if the logger already has handlers
        if not self.logger.handlers:
            self.setup_logger(console_log, file_log)

    def setup_logger(self, console_log, file_log):
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        if file_log:
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            file_handler = RotatingFileHandler(self.log_file, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(self.level)
            self.logger.addHandler(file_handler)
        if console_log:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(self.level)
            self.logger.addHandler(console_handler)

    def log_here(self, level, msg):
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(msg)  # The logger will handle both console and file output

    def log_debug(self, msg): self.log_here('debug', msg)
    def log_info(self, msg): self.log_here('info', msg)
    def log_warning(self, msg): self.log_here('warning', msg)
    def log_error(self, msg): self.log_here('error', msg)
    def log_critical(self, msg): self.log_here('critical', msg)

    def log_exception(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.log_error_with_traceback(e, func.__name__)
                raise
        return wrapper

    def log_error_with_traceback(self, exception, function_name):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = traceback.extract_tb(exc_traceback)
        if not self.include_logger_in_traceback:
            filtered_tb = [
                entry for entry in tb if entry.filename.split(os.sep)[-1] != self.logger_filename
            ]
        else:
            filtered_tb = tb
        formatted_tb = traceback.format_list(filtered_tb)
        formatted_error = "Traceback (most recent call last):\n" + "".join(formatted_tb) + f"{exc_type.__name__}: {exc_value}"
        # Use logger.error with exc_info to automatically include the traceback
        self.logger.error(f"Exceção capturada no decorador - {function_name}\n{formatted_error}", exc_info=False)

# Configura o logger padrão
default_logger = CustomLogger(
    name='DefaultLogger',
    level=logging.DEBUG,
    console_log=True,
    file_log=True,
    logger_filename='logger.py',
    include_logger_in_traceback=False
)


"""
Níveis Hierárquicos de Log:
DEBUG (10): Tudo será registrado.
INFO (20): Registra INFO, WARNING, ERROR, CRITICAL.
WARNING (30): Registra apenas WARNING, ERROR, CRITICAL.
ERROR (40): Registra apenas ERROR e CRITICAL.
CRITICAL (50): Registra apenas CRITICAL.
"""
