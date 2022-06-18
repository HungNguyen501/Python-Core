import os
from os.path import join, dirname
from dotenv import find_dotenv, load_dotenv

dotenv_path = join(dirname(__file__), ".env")
print(dotenv_path)
# print(__file__)

load_dotenv(dotenv_path=dotenv_path)

USER_NAME = os.environ.get("USER_NAME")
PASSWORD = os.environ.get("PASSWORD")

print(USER_NAME)
print(PASSWORD)