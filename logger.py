import logging
from logging.handlers import RotatingFileHandler
import os
from functools import wraps
import traceback
import sys
import inspect

class CustomLogger:
    def __init__(self, name='FoxCoffe', log_file='logError.log', level=logging.INFO, console_log=True, file_log=True, logger_filename='logger.py', include_logger_in_traceback=False):
        self.log_file = os.path.join(os.getcwd(), log_file)
        self.logger = logging.getLogger(name)
        self.level = level
        self.logger_filename = logger_filename
        self.include_logger_in_traceback = include_logger_in_traceback
        self.logger.setLevel(self.level)
        if not self.logger.handlers:
            self.setup_logger(console_log, file_log)

    def setup_logger(self, console_log, file_log):
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
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

    def get_stacklevel(self):
        """
        Calcula dinamicamente o stacklevel com base na pilha de chamadas atual.
        """
        stack = inspect.stack()
        stacklevel = 1
        for frame_info in stack[1:]:
            module_name = frame_info.frame.f_globals.get('__name__', '')
            if module_name != __name__:
                break
            stacklevel += 1
        return stacklevel

    def log_here(self, level, msg, *args, **kwargs):
        """
        Registra mensagens de log em diferentes níveis e aceita argumentos adicionais.
        """
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        if 'stacklevel' in kwargs:
            kwargs['stacklevel'] += 1
        else:
            kwargs['stacklevel'] = self.get_stacklevel()
        log_method(msg, *args, **kwargs)

    def log_debug(self, msg, *args, **kwargs):
        self.log_here('debug', msg, *args, **kwargs)

    def log_info(self, msg, *args, **kwargs):
        self.log_here('info', msg, *args, **kwargs)

    def log_warning(self, msg, *args, **kwargs):
        self.log_here('warning', msg, *args, **kwargs)

    def log_error(self, msg, *args, **kwargs):
        self.log_here('error', msg, *args, **kwargs)

    def log_critical(self, msg, *args, **kwargs):
        self.log_here('critical', msg, *args, **kwargs)

    def log_exception(self, func):
        """
        Decorador para registrar exceções levantadas dentro da função decorada.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.log_error_with_traceback(e, func.__name__)
                raise
        return wrapper

    def log_error_with_traceback(self, exception, function_name):
        """
        Registra um traceback detalhado do erro.
        """
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = traceback.extract_tb(exc_traceback)

        # Filtra o traceback se include_logger_in_traceback for False
        if not self.include_logger_in_traceback:
            filtered_tb = [
                entry for entry in tb if entry.filename.split(os.sep)[-1] != self.logger_filename
            ]
        else:
            filtered_tb = tb

        formatted_tb = traceback.format_list(filtered_tb)
        formatted_error = "Traceback (most recent call last):\n" + "".join(formatted_tb) + f"{exc_type.__name__}: {exc_value}"

        # Registra o erro com o stacklevel correto
        self.logger.error(
            f"Exception in function '{function_name}':\n{formatted_error}",
            exc_info=False,
            stacklevel=self.get_stacklevel()
        )

    def set_level(self, level):
        """
        Atualiza dinamicamente o nível de log para todos os handlers.
        """
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)

    @staticmethod
    def from_config(config):
        """
        Cria um logger a partir de um dicionário de configuração externo.
        """
        return CustomLogger(
            name=config.get('name', 'DefaultLogger'),
            log_file=config.get('log_file', 'logError.log'),
            level=config.get('level', logging.INFO),
            console_log=config.get('console_log', True),
            file_log=config.get('file_log', True),
            logger_filename=config.get('logger_filename', 'logger.py'),
            include_logger_in_traceback=config.get('include_logger_in_traceback', False)
        )

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
