
import os
import asyncio
from dotenv import load_dotenv
from common.gdb_helper import GDBConnection
from models.user import User
from controllers.subscription import Subscription


async def main():
    load_dotenv(verbose=True)

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

    gdb.close()

    return


if __name__ == "__main__":

    asyncio.run(main())
