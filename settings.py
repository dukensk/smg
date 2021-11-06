import os
from os.path import join, dirname
from dotenv import load_dotenv

from smg.service import get_system_downloads_path

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SAVE_PATH = os.environ.get('SAVE_PATH', default=get_system_downloads_path())
'''Путь для сохранения скачанных файлов'''

TRANSLATOR_SAVE_PATH = SAVE_PATH + '/translator'
TRANSLATOR_TEMP_PATH = TRANSLATOR_SAVE_PATH + '/temp'

TRANSLATOR_VOLUME_ORIGINAL_AUDIO = 0.25
TRANSLATOR_OUTPUT_AUDIO_BITRATE = '192k'
