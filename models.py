from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Base = declarative_base()

class LinkPage(Base):
    __tablename__ = 'LinkPage'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    bio= Column(String(255))
    image= Column(String(255))

class Link(Base):
    __tablename__ = 'Link'
    id = Column(Integer, primary_key=True)
    page_id = Column(Integer, ForeignKey('LinkPage.id'))
    name = Column(String(255))
    url = Column(String(255))
    category = Column(String(255))

