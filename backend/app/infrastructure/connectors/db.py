from sqlalchemy import create_engine
from retry import retry
import time

@retry(tries=3, delay=2)
def get_engine():
    time.sleep(2)
    engine = create_engine('mysql+mysqlconnector://user:user@db:3306/todolist')

    return engine.connect()

