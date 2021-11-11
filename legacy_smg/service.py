import os
import sys
import io

from legacy_smg.preset import OutputFormat, OutputFormatMenu


def show_app_header():
    """Выводит заголовок приложения"""
    print('Simple Media Grabber by Duke\n')


def choose_output_format(format_menu: OutputFormatMenu) -> OutputFormat:
    """Выбирает выходной формат из меню на основе ввода пользователя"""
    print('\n' + str(format_menu))
    output_format = None if not format_menu.is_empty else format_menu.default_output_format

    while not output_format:
        try:
            preset_index = int(
                input('\nВыберите предпочтительный формат для скачивания [{min_index}-{max_index}]: '
                      .format(min_index=format_menu.min_index, max_index=format_menu.max_index))
            )
            output_format = format_menu.get_format_preset_by_index(preset_index)
        except ValueError:
            print("Вы ввели некорректное значение. Необходимо ввести число в диапазоне от {min_index} до {max_index}"
                  .format(min_index=format_menu.min_index, max_index=format_menu.max_index))
        except IndexError:
            print('Пункта меню с таким номером не существует. Необходимо ввести число в диапазоне от {min_index} до {max_index}'
                  .format(min_index=format_menu.min_index, max_index=format_menu.max_index))

    clear_console()
    # show_app_header()
    print('Выбран формат: {output_format}\n'.format(output_format=str(output_format)))
    return output_format


def clear_console():
    """Очищает консоль"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_system_downloads_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')


def force_terminal_unicode_encoding():
    """Принудительно переключаем кодировку вывода терминале в UTF-8, чтобы не было проблем с кириллицей"""
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
