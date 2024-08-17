import os
from pathlib import Path
from dotenv import load_dotenv

from common.filesystem import get_system_downloads_path

ROOT_PATH = Path(__file__).resolve().parent
'''Path to the root of the application'''

dotenv_path = ROOT_PATH / '.env'
load_dotenv(str(dotenv_path))

SAVE_PATH = Path(os.environ.get('SAVE_PATH', default=get_system_downloads_path()))
'''Path to save downloaded files'''

TEMP_PATH = Path(os.environ.get('TEMP_PATH', default=SAVE_PATH / 'temp'))
'''Path for temporary files'''

TRANSLATOR_SAVE_PATH = os.environ.get('TRANSLATOR_SAVE_PATH', default=SAVE_PATH)
'''Path for translated files'''

TRANSLATOR_VOLUME_ORIGINAL_AUDIO = 0.45

TRANSLATOR_OUTPUT_AUDIO_BITRATE_IN_VIDEOFILE = '192k'
TRANSLATOR_OUTPUT_AUDIO_BITRATE_IN_AUDIOFILE = '128k'
TRANSLATOR_VOLUME_BOOST = '8dB'

DOWNLOAD_ATTEMPTS_LIMIT = 20

MEDIAGRABBER_DOWNLOAD_ATTEMPTS_LIMIT = 20

ENABLE_PUSH_NOTIFICATION = os.environ.get('ENABLE_PUSH_NOTIFICATION', default=True)
'''Allows system push notifications'''

ICONS_PATH = ROOT_PATH / 'icons'
