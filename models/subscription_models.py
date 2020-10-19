
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, String, Float, Text

Base = declarative_base()
DEFAULT_TABLE_ARGS = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8', 'mysql_collate': 'utf8_general_ci'}


class Subscription(Base):
    __tablename__ = "subscriptions"
    __table_args__ = DEFAULT_TABLE_ARGS
    __primary_key__ = 'subscription_id'

    subscription_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
