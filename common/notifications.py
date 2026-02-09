import os
import platform

import settings


def show_push_notification(title: str, message: str, icon: str = 'smg_icon.ico', app_id: str = 'SMG') -> bool:
    """
    Shows system push notifications
    :param app_id:
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
        '''  # noqa: Q001
    elif platform_name == 'Linux':
        command = f'''
        notify-send "{title}" "{message}" --icon="{icon_path}"
        '''  # noqa: Q001
    elif platform_name == 'Windows':
        from winotify import Notification
        toast = Notification(app_id=app_id, title=title, msg=message, icon=icon_path)
        toast.show()
        return True
    else:
        return True
    os.system(command)
