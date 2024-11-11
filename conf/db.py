import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

user = config.get('DEV_DB', 'user')
password = config.get('DEV_DB', 'password')
domain = config.get('DEV_DB', 'domain')
port = config.get('DEV_DB', 'port')
db = config.get('DEV_DB', 'db')

URI = f'postgresql://{user}:{password}@{domain}:{port}/{db}'

engine = create_engine(URI, echo=False, pool_size=5, max_overflow=0)
DBSession = sessionmaker(bind=engine)
session = DBSession()
