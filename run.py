#!/opt/chi/python/bin/python
import os
from dotenv import load_dotenv


def main():
    load_dotenv(verbose=True)
    print(f"Version: {os.environ.get('VERSION')}")
    print('hello world!')


if __name__ == "__main__":
    main()
