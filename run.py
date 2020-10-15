#!/opt/chi/python/bin/python

import os
import time
import asyncio
from dotenv import load_dotenv
from common.gdb_helper import GDBConnection
from models.user import User


async def db_test():
    # connect to db
    config = {
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST_MAIN'),
        'database': os.environ.get('DB_NAME'),
    }
    gdb = GDBConnection(config)

    query = gdb.query(User)
    resp = await gdb.all(query)
    print(resp)

    # create user object
    # user = User()
    # user.name = 'Munib 2'
    # user.phone = '000'
    # user.address = 'Islamabad'
    # await gdb.add(user)
    # await gdb.commit()

    gdb.close()


async def func1():
    t1 = int(time.time())
    t2 = t1
    while t2 - t1 < 30:  # diff less than 30 sec
        await asyncio.sleep(1)
        t2 = int(time.time())
        print('func 1')
    print('func 1 completed ............')


async def func2():
    t1 = int(time.time())
    t2 = t1
    while t2 - t1 < 5:  # diff less than 30 sec
        await asyncio.sleep(1)
        t2 = int(time.time())
        print('func 2')
    print('func 2 completed ............')


async def main():
    await asyncio.sleep(1)
    load_dotenv(verbose=True)
    print(f"Version: {os.environ.get('VERSION')}")
    # print('hello world!')

    await asyncio.gather(
        func1(),
        func2()
    )

    print('=== done ===')
    return


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # try:
    #     loop.run_until_complete(main())
    # finally:
    #     loop.close()

    asyncio.run(main())
