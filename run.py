#!/opt/chi/python/bin/python

from dotenv import load_dotenv


def main():
    load_dotenv(verbose=True)
    print('hello world!')


if __name__ == "__main__":
    main()
