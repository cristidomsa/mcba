import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///test.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)

session = None
def get_session():
    global session
    if session is None:
        #Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        session = Session()
    return session