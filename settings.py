import os
from pathlib import Path
from dotenv import load_dotenv

from common.filesystem import get_system_downloads_path

dotenv_path = Path(__file__).resolve().parent / '.env'
load_dotenv(str(dotenv_path))

SAVE_PATH = Path(os.environ.get('SAVE_PATH', default=get_system_downloads_path()))
'''Path to save downloaded files'''

TEMP_PATH = Path(os.environ.get('TEMP_PATH', default=SAVE_PATH / 'temp'))
'''Path for temporary files'''

TRANSLATOR_SAVE_PATH = os.environ.get('TRANSLATOR_SAVE_PATH', default=SAVE_PATH)
'''Path for translated files'''

TRANSLATOR_VOLUME_ORIGINAL_AUDIO = 0.45
TRANSLATOR_OUTPUT_AUDIO_BITRATE = '192k'
TRANSLATOR_VOLUME_BOOST = '8dB'

DOWNLOAD_ATTEMPTS_LIMIT = 3

ENABLE_PUSH_NOTIFICATION = os.environ.get('ENABLE_PUSH_NOTIFICATION', default=True)
'''Allows system push notifications'''

ICONS_PATH = Path(__file__).resolve().parent / 'icons'
