# Filename: connector.py
# Created By: Munib
# Created On: 14-Oct-2020 03:37pm

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Connector:
    def __init__(self, config):
        self.config = config
        self.gdb = None

    def connect(self):
        print('connecting ...')
        db_Url = 'mysql+mysqlconnector://{user}:{password}@{host}/{database}'.format(**self.config)
        engine = create_engine(db_Url, echo=0, pool_recycle=1800)
        print(db_Url)
        session_maker = sessionmaker(bind=engine)
        self.gdb = session_maker()
        if self.gdb is not None:
            print('connected!')

        return

    def add(self, rec):
        self.gdb.add(rec)
        self.gdb.flush()
        return rec

    def commit(self):
        self.gdb.commit()

    def disconnect(self):
        self.gdb.close()
