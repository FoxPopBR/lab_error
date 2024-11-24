import logging
from logging.handlers import RotatingFileHandler
import os
from functools import wraps
from datetime import datetime

class CustomLogger:
    """
    Classe CustomLogger unificada para configuração e registro de logs.
    Combina a simplicidade de configuração da versão atual com os métodos e funcionalidades personalizadas da versão antiga.
    """

    def __init__(self, name='FoxCoffe', log_file='logError.log', level=logging.INFO, console_log=True, file_log=True):
        """
        Inicializa o logger com as configurações especificadas.

        :param name: Nome do logger.
        :param log_file: Nome do arquivo de log (salvo no diretório de execução atual).
        :param level: Nível de log padrão.
        :param console_log: Ativar/desativar logs no console.
        :param file_log: Ativar/desativar logs em arquivo.
        """
        # Caminho completo para o arquivo de log no diretório atual
        self.log_file = os.path.join(os.getcwd(), log_file)
        self.logger = logging.getLogger(name)
        self.level = level

        # Configura o logger
        self.setup_logger(console_log, file_log)

    def setup_logger(self, console_log, file_log):
        """
        Configura o logger com handlers de arquivo e console.
        """
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Configuração do arquivo de log
        if file_log and not any(isinstance(handler, RotatingFileHandler) for handler in self.logger.handlers):
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)  # Cria diretórios, se necessário
            file_handler = RotatingFileHandler(self.log_file, maxBytes=5*1024*1024, backupCount=3)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(self.level)
            self.logger.addHandler(file_handler)

        # Configuração do console
        if console_log and not any(isinstance(handler, logging.StreamHandler) for handler in self.logger.handlers):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(self.level)
            self.logger.addHandler(console_handler)

    def format_message(self, msg):
        """
        Formata a mensagem para adicionar informações adicionais, se necessário.
        """
        return f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}"

    def log_here(self, level, msg):
        """
        Registra o log conforme o nível especificado.
        """
        formatted_msg = self.format_message(msg)
        getattr(self.logger, level.lower(), self.logger.info)(formatted_msg)

    # Métodos simplificados para diferentes níveis de log
    def log_debug(self, msg): self.log_here('debug', msg)
    def log_info(self, msg): self.log_here('info', msg)
    def log_warning(self, msg): self.log_here('warning', msg)
    def log_error(self, msg): self.log_here('error', msg)
    def log_critical(self, msg): self.log_here('critical', msg)

    @staticmethod
    def log_exception(func):
        """
        Decorador para registrar exceções automaticamente.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Assume que o primeiro argumento é a instância de CustomLogger
                logger = args[0].logger if args else logging.getLogger(__name__)
                logger.error(f"Exceção em {func.__name__}: {str(e)}", exc_info=True)
                raise
        return wrapper


# Configura o logger padrão
default_logger = CustomLogger(name='DefaultLogger', level=logging.DEBUG, console_log=True, file_log=True)

"""
Níveis Hierárquicos de Log:
DEBUG (10): Tudo será registrado.
INFO (20): Registra INFO, WARNING, ERROR, CRITICAL.
WARNING (30): Registra apenas WARNING, ERROR, CRITICAL.
ERROR (40): Registra apenas ERROR e CRITICAL.
CRITICAL (50): Registra apenas CRITICAL.
"""
