#!/opt/chi/python/bin/python
import os
from dotenv import load_dotenv
from common.connector import Connector
from models.user import User


def main():
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
    db = Connector(config)
    try:
        db.connect()
    except Exception as ex:
        print(f'Connection Error: {ex}')
        return

    # create user object
    user = User()
    user.name = 'Munib'
    user.phone = '000'
    user.address = 'Islamabad'

    # add to db
    db.add(user)

    db.commit()

    db.disconnect()


if __name__ == "__main__":
    main()

