
import time
import asyncio
import concurrent.futures
from sqlalchemy.orm import Session, Query
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect


QUERY_MAX_TIME = 0.04


class GDBQuery(Query):

    def __init__(self, entities, session=None):
        super().__init__(entities, session)

    @property
    def model_class(self):
        return self._mapper_zero().class_

    @property
    def primary_key(self):
        # get the primary key column
        ins = inspect(self.model_class)
        return ins.primary_key[0]

    def get(self, ident):
        col = getattr(self.model_class, self.model_class.__primary_key__)
        self = self.filter(col == ident)
        resp = self.one_or_none()
        return resp

    def one_or_none(self):
        t1 = time.time()
        resp = super().one_or_none()
        td = time.time() - t1
        if td > QUERY_MAX_TIME:
            self.print('one_or_none', td)
        return resp

    def all(self):
        t1 = time.time()
        resp = super().all()
        td = time.time() - t1
        if td > QUERY_MAX_TIME:
            self.print('all', td)
        return resp

    def update(self, values, synchronize_session="evaluate", update_args=None):
        return super().update(values, synchronize_session, update_args)

    def delete(self, synchronize_session="evaluate"):
        t1 = time.time()
        resp = super().delete(synchronize_session)
        td = time.time() - t1
        if td > QUERY_MAX_TIME:
            self.print('delete', td)
        return resp

    def print(self, func=None, td=None):
        print(f'query -> {func} ({round(td, 3)} ms) \r\n{str(self.statement.compile(compile_kwargs={"literal_binds": True}))}')
        return


class GDBSession(Session):

    def __init__(self, bind=None, autoflush=True, expire_on_commit=True, _enable_transaction_accounting=True,
                 autocommit=False, twophase=False, weak_identity_map=None, binds=None, extension=None,
                 enable_baked_queries=True, info=None, query_cls=GDBQuery):
        super().__init__(bind, autoflush, expire_on_commit, _enable_transaction_accounting, autocommit, twophase,
                         weak_identity_map, binds, extension, enable_baked_queries, info, query_cls)

    def add(self, instance, _warn=True):
        super().add(instance, _warn)

    def delete(self, instance):
        super().delete(instance)

    def execute(self, clause, params=None, mapper=None, bind=None, **kw):
        t1 = time.time()
        resp = super().execute(clause, params, mapper, bind, **kw)
        td = time.time() - t1
        if td > QUERY_MAX_TIME:
            print(f'gdb -> execute ({round(td, 3)} ms) \r\n{str(clause.compile(compile_kwargs={"literal_binds": True}))}')
        return resp


class GDBConnection:
    def __init__(self, config):
        self.Config = config
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)
        # self.loop = tornado.ioloop.IOLoop.current()
        self.loop = asyncio.get_event_loop()
        self.db_session = None
        self.connect()

    def connect(self):
        db_url = 'mysql+mysqlconnector://{user}:{password}@{host}/{database}'.format(**self.Config)
        print('DB =', self.Config['database'])

        db_engine = create_engine(db_url, echo=False, pool_recycle=3600)
        self.db_session: Session = sessionmaker(bind=db_engine, class_=GDBSession)()

    def query(self, *models) -> Query:
        return self.db_session.query(*models)

    async def execute(self, statement):
        res = await self.loop.run_in_executor(self.executor, self.db_session.execute, statement)
        return res

    async def add(self, model):
        res = await self.loop.run_in_executor(self.executor, self.db_session.add, model)
        return res

    async def one_or_none(self, query: Query):
        res = await self.loop.run_in_executor(self.executor, query.one_or_none)
        return res

    async def all(self, query: Query):
        res = await self.loop.run_in_executor(self.executor, query.all)
        return res

    async def delete(self, query: Query):
        await self.loop.run_in_executor(self.executor, query.delete)

    async def flush(self):
        await self.loop.run_in_executor(self.executor, self.db_session.flush)

    async def commit(self):
        await self.loop.run_in_executor(self.executor, self.db_session.commit)

    async def rollback(self):
        await self.loop.run_in_executor(self.executor, self.db_session.rollback)

    def close(self):
        self.db_session.close()
