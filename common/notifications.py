import os
import platform
from win10toast import ToastNotifier
import settings


def show_push_notification(title: str, message: str, icon: str = 'smg_icon.ico') -> bool:
    """
    Shows system push notifications
    :param title: title of the message
    :param message: message text
    :param icon: name of the icon file from the icons directory
    :return:
    """
    if not settings.ENABLE_PUSH_NOTIFICATION:
        return False

    platform_name = platform.system()
    icon_path = settings.ICONS_PATH / icon

    if platform_name == 'Darwin':
        command = '''
        osascript -e 'display notification "{message}" with title "{title}"'
        '''
    elif platform_name == 'Linux':
        command = f'''
        notify-send "{title}" "{message}" --icon="{icon_path}"
        '''
    elif platform_name == 'Windows':
        ToastNotifier().show_toast(title, message, icon_path)
        return True
    else:
        return True
    os.system(command)
