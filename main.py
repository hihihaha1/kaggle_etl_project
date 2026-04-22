from sqlalchemy import create_engine
from logger_config import setup_logger
import time
import pandas as pd
import os

logger = setup_logger()

def extract_data(filename):
    logger.info(f"Начинается извлечение данных из {filename}")

    if not os.path.exists(filename):
        logger.error(f"Файл {filename} не найден")
        return None

    try:
        df = pd.read_csv(filename, nrows=1000)
        logger.info(f"Файл {filename} успешно считан")
        logger.info(f"Считаны колонки: {df.columns.tolist()}")
        return df
    except Exception as e:
        logger.error(f"Файл {filename} не удалось считать. {e}")
        return None

def transform_data(df):
    logger.info("Начало Transform")
    init_len = len(df)
    df = df.drop_duplicates().copy()
    df['amount'] = df['amount'].fillna(0)
    clear_len = len(df)
    logger.info(f"Убрано {init_len - clear_len} дубликатов")
    mask_amount = df['amount'] > 0
    df = df[mask_amount]
    logger.info(f"Итоговое количество строк без дубликатов, NaN и некорректной суммой: {len(df)}")
    logger.info("Trasform завершен")

    mapping = {
        'nameOrig' : 'name_orig',
        'oldbalanceOrg': 'old_balance_org',
        'newbalanceOrig': 'new_balance_orig',
        'nameDest': 'name_dest',
        'oldbalanceDest': 'old_balance_dest',
        'newbalanceDest': 'new_balance_dest',
        'isFraud': 'is_fraud',
        'isFlaggedFraud': 'is_flagged_fraud'
    }

    df = df.rename(columns=mapping)

    logger.info("Колонки переименованы")
    return  df

def load_data(df):
    logger.info("Начало Load")
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        DATABASE_USER = 'kaggle_pet'
        DATABASE_PASSWORD = 'secretpassword'
        DATABASE_DB = 'kaggle_table'
        DATABASE_HOST = 'db'
        DATABASE_PORT = '5432'
        DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"
    engine = create_engine(DATABASE_URL)

    max_retries = 5
    for i in range(max_retries):
        try:
            with engine.connect() as conn:
                logger.info("Попытка подключиться к базе")
                break
        except Exception:
            logger.info("База еще не запущена. Повторная попытка через 5 сек.")
            time.sleep(5)
    else:
        logger.error("Не удалось подключиться к базе")
        return

    try:
        logger.info("Попытка записать данные в таблицу")
        table_name = 'transactions'
        df_to_save = df.reset_index() if df.index.name else df
        df_to_save.to_sql(table_name, engine, if_exists='append', index=False)
        logger.info("Load данных закончен успешно")
    except Exception as e:
        logger.error(f"Ошибка записи данных. {e}")

if __name__ == "__main__":
    DATA_PATH = '/app/data/creditcard.csv'

    df = extract_data(DATA_PATH)
    if df is not None:
        logger.info("Extract завершен")
        df = transform_data(df)
        load_data(df)
