import logging
import sys
import os

def setup_logger():
    # Папка с логами
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Логгер и задаем уровень DEBUG
    logger = logging.getLogger("ETL-logger")
    logger.setLevel(logging.DEBUG)

    # Задаем формат вывода в логах
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    # Обработчик логов в консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Обработчик логов в файл
    file_handler = logging.FileHandler(os.path.join(log_dir, 'etl.log'))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Привязываем к логгеру
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger