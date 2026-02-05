from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

engine = create_engine("sqlite:///app.db")
sessionlocal = sessionmaker(bind=engine)
session = sessionlocal()
Base.metadata.create_all(engine)
