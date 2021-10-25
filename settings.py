import os
from os.path import join, dirname
from dotenv import load_dotenv

from smg.service import get_system_downloads_path

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SAVE_PATH = os.environ.get('SAVE_PATH', default=get_system_downloads_path())
'''Путь для сохранения скачанных файлов'''

