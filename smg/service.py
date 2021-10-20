import os

from smg.preset import OutputFormat, OutputFormatMenu


def show_app_header():
    """Выводит заголовок приложения"""
    print('Simple Media Grabber by Duke\n')


def choose_output_format(format_menu: OutputFormatMenu) -> OutputFormat:
    """Выбирает выходной формат из меню на основе ввода пользователя"""
    print('\n' + str(format_menu))
    output_format = None

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
    show_app_header()
    print('Выбран формат: {output_format}\n'.format(output_format=str(output_format)))
    return output_format


def clear_console():
    """Очищает консоль"""
    os.system('cls' if os.name == 'nt' else 'clear')


def download_complete_hook(d):
    if d['status'] == 'finished':
        print('Скачивание завершено, запускаем постобработку...')
