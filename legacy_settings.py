import os
from os.path import join, dirname
from dotenv import load_dotenv

from legacy_smg.service import get_system_downloads_path

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SAVE_PATH = os.environ.get('SAVE_PATH', default=get_system_downloads_path())
'''Путь для сохранения скачанных файлов'''

TRANSLATOR_SAVE_PATH = SAVE_PATH
TRANSLATOR_TEMP_PATH = TRANSLATOR_SAVE_PATH + '/temp'

TRANSLATOR_VOLUME_ORIGINAL_AUDIO = 0.45
TRANSLATOR_OUTPUT_AUDIO_BITRATE = '192k'
TRANSLATOR_VOLUME_BOOST = '8dB'

TRANSLATOR_DOWNLOAD_ATTEMPTS_LIMIT = 3