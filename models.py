from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

db = sqlalchemy.create_engine('sqlite:///passwords.db')


class Service(Base):
    __tablename__ = 'services'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    id = Column(Integer, primary_key=True)
    service_name = Column(String(length=32), unique=True)
    username = Column(String(length=32))
    password_hash = Column(String(length=256))

    user = relationship('User', back_populates='service')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(length=32), unique=True)
    key = Column(String(length=256))
    salt = Column(String(length=16))
    service = relationship('Service', back_populates='user')

    def __repr__(self):
        return f'<{self.id}|{self.username}>'


Base.metadata.create_all(db)

Session = sqlalchemy.orm.sessionmaker(bind=db)
session = Session()