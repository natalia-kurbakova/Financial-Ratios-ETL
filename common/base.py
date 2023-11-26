from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
import Keys
import os

os.environ['connect_str'] = Keys.connect_str

engine = create_engine(os.environ['connect_str'], connect_args={'dialect':'mssql'})
session = Session(engine)
Base = declarative_base()