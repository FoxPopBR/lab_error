#lib_error.py
from datetime import datetime
import os
import logging
import logging.config
import traceback
import json
from functools import wraps
from logging.handlers import TimedRotatingFileHandler

class CustomLogger:
    """
    Classe CustomLogger unificada para configuração e registro de logs.
    Esta classe configura o logger, incluindo formatação e rotação de arquivos de log.
    """

    def __init__(self,terminal_notifications=None, log_file_path='app_errors.log', config_file='logging_config.json', log_level=logging.INFO):
        self.log_file_path = log_file_path
        self.config_file = config_file
        self.log_level = log_level
        self.terminal_notifications = terminal_notifications if terminal_notifications else {}
        self.logger = logging.getLogger(__name__)
        self.setup_logger()

    def load_configuration(self):
        """
        Carrega a configuração de logging a partir de um arquivo JSON.
        """
        try:
            with open(self.config_file, 'r') as file:
                config = json.load(file)
                # Personaliza o caminho do arquivo de log se necessário
                for handler in config['handlers'].values():
                    if 'filename' in handler:
                        handler['filename'] = self.log_file_path
            logging.config.dictConfig(config)
        except Exception as e:
            print(f"Erro ao carregar configuração de logging: {e}. Aplicando configuração de fallback.")
            # Implemente aqui uma configuração de fallback se necessário

    def apply_fallback_configuration(self):
        """
        Aplica uma configuração de fallback para o logger.
        """
        self.logger.setLevel(self.log_level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def format_message(self, msg):
        """
        Formata a mensagem de log. Esta implementação é apenas um exemplo e pode ser adaptada conforme necessário.
        """
        # Exemplo simples de formatação. Pode ser personalizado conforme necessário.
        return f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}"

    def ensure_log_directory_exists(self):
        """
        Verifica se o diretório para o arquivo de log existe, se não, cria o diretório.
        """
        log_dir = os.path.dirname(self.log_file_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def setup_logger(self):
        self.load_configuration()
        if not self.logger.handlers:
            self.ensure_log_directory_exists()
            file_handler = TimedRotatingFileHandler(self.log_file_path, when="midnight", interval=1)
            file_handler.suffix = "%Y-%m-%d_%H-%M-%S.log"
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)'))
            self.logger.addHandler(file_handler)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)'))
            self.logger.addHandler(console_handler)

    def log_here(self, level, msg):
        """
        Registra o log conforme o nível especificado e verifica notificação no terminal.
        """
        formatted_msg = self.format_message(msg)  # Formata a mensagem antes de registrá-la
        getattr(self.logger, level.lower(), self.logger.info)(formatted_msg)
        if self.terminal_notifications.get(level.lower(), False):
            print(f"Terminal Log ({level.upper()}): {formatted_msg}")

    # Métodos simplificados de log
    def log_debug(self, message_key): self.log_here('debug', message_key)
    def log_info(self, message_key): self.log_here('info', message_key)
    def log_warning(self, message_key): self.log_here('warning', message_key)
    def log_error(self, message_key): self.log_here('error', message_key)
    def log_critical(self, message_key): self.log_here('critical', message_key)

    @staticmethod
    def log_exception(func):
        """
        Decorador que registra exceções.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Assume que o primeiro argumento de args é a instância de CustomLogger
                logger = args[0].logger if args else logging.getLogger(__name__)
                logger.error(f"Exceção em {func.__name__}: {str(e)}", exc_info=True)
                raise
        return wrapper

# O decorador para log de exceções continua correto e não necessita de ajustes.

# Exemplo de uso da classe CustomLogger
if __name__ == "__main__":
    custom_logger = CustomLogger()
    custom_logger.log_info("Este é um log de informação")
    custom_logger.log_error("Este é um log de erro")
