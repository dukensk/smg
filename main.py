import sys

import colorama
import yt_dlp
from colorama import init, Fore, Back, Style

import settings
import smg.preset
from smg.preset import OutputFormatMenu
from smg.service import show_app_header, choose_output_format, clear_console

if __name__ == '__main__':
    # Принудительно переключаем кодировку вывода консоли в UTF-8, чтобы не было проблем с кириллицей
    sys.stdout.reconfigure(encoding='utf-8')

    while True:
        colorama.init(autoreset=True)
        show_app_header()

        video_url = input('Введите URL видео: ')

        output_format_menu = OutputFormatMenu(smg.preset.output_formats)
        output_format = choose_output_format(output_format_menu)

        ydl_opts = {
            'noplaylist': True,
            'format': output_format.preset,
            'outtmpl': settings.SAVE_PATH + '/%(title)s.%(ext)s',
            'concurrent-fragments': 3,
        }

        if output_format.postprocessors:
            ydl_opts['postprocessors'] = output_format.postprocessors

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            print(Style.DIM + Fore.GREEN + '\nГотово' + Style.RESET_ALL)
            print('Все операции успешно завершены. Можно скачать что-нибудь еще.')
        except yt_dlp.DownloadError:
            print(Style.DIM + Fore.RED + '\n\nYOU DIED' + Style.RESET_ALL)
            print('\nНе удалось скачать видео. Нам очень жаль. :('
                  '\nТак бывает, если оно еще не до конца обработалось на сервисе или вы ввели неправильную ссылку. '
                  'Попробуйте позже.')

        input('\nДля продолжения нажмите ENTER...')
        clear_console()
