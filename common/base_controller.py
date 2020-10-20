
from common.gdb_helper import GDBConnection


class Context:

    gdb: GDBConnection
    handler: None  # request handler
    data = {}
    files = {}
    session = {}

    def __init__(self):
        pass


class BaseController:

    gdb = None
    model = None  # sqlalchemy model

    def __init__(self, ctx: Context):
        self.gdb = ctx.gdb
        self.context = ctx
        return

    async def create(self):

        rec = self.model()

        for k, v in self.context.data.items():
            if isinstance(v, str) and v == '':
                v = None

            attr = getattr(self.model, k, None)
            if attr is not None:
                setattr(rec, k, v)

        await self.gdb.add(rec)
        await self.gdb.flush()

        rec_id = getattr(rec, self.model.__primary_key__)
        return rec_id

    async def all(self):
        query = self.gdb.query(self.model)
        resp = await self.gdb.all(query)
        return resp
