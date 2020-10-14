# Filename: user.py
# Created By: Munib
# Created On: 14-Oct-2020 03:37pm

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, String, Float, Text

Base = declarative_base()
DEFAULT_TABLE_ARGS = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8', 'mysql_collate': 'utf8_general_ci'}


class User(Base):
    __tablename__ = "users"
    __table_args__ = DEFAULT_TABLE_ARGS
    __primary_key__ = 'user_id'

    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(128), nullable=False)
    phone = Column(String(11), nullable=True)
    address = Column(String(512), nullable=True)


# class User:
#
#     def __init__(self, name, phone, address):
#         self.name = name
#         self.phone = phone
#         self.address = address
#         return
#
#     def print(self):
#         print(f'Name: {self.name}, Phone: {self.phone}, Address: {self.address}')
#         return
