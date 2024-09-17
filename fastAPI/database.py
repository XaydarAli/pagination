from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

ENGINE = create_engine('postgresql://postgres:Alijon1308@localhost/insta', echo=True)
Base = declarative_base()
Session = sessionmaker()
