#!/opt/chi/python/bin/python

import asyncio

import os
from dotenv import load_dotenv
from common.gdb_helper import GDBConnection
from models.user import User


async def main():
    await asyncio.sleep(1)
    load_dotenv(verbose=True)
    print(f"Version: {os.environ.get('VERSION')}")
    # print('hello world!')

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
    # user.name = 'Munib 1'
    # user.phone = '000'
    # user.address = 'Islamabad'

    # add to db
    # db.add(user)
    #
    # db.commit()
    #
    # db.disconnect()


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # loop.run_in_executor()
    # try:
    #     loop.run_until_complete(main())
    # finally:
    #     loop.close()

    asyncio.run(main())


