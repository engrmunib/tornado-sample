
import os
import asyncio
from dotenv import load_dotenv
from common.gdb_helper import GDBConnection
from controllers.user_controller import UserController
from common.base_controller import Context

from sqlalchemy import func


async def main():
    load_dotenv(verbose=True)

    config = {
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST_MAIN'),
        'database': os.environ.get('DB_NAME'),
    }
    gdb = GDBConnection(config)

    ctx = Context()
    ctx.gdb = gdb

    ctrl = UserController(ctx)

    ctx.data = {
        'username': 'munib',
        'password': func.md5('munib'),
        'name': 'Munib'
    }
    # resp = await ctrl.create()
    # print(resp)

    resp = await ctrl.all()
    print(resp)

    await gdb.commit()
    gdb.close()

    return


if __name__ == "__main__":

    asyncio.run(main())
