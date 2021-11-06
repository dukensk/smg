import colorama
import wget
import yt_dlp
from colorama import Fore, Style
from smg.preset import OutputFormatMenu
import settings
import translator.preset

from smg.service import force_terminal_unicode_encoding, choose_output_format, clear_console
from translator.service import show_app_header, merge_video_and_vo


def main():
    force_terminal_unicode_encoding()
    colorama.init(autoreset=True)
    output_format_menu = OutputFormatMenu(translator.preset.output_formats)

    while True:
        show_app_header()
        video_url = input('Введите URL видео: ')
        output_format = choose_output_format(output_format_menu)

        vo_url = input('Введите URL VO: ')
        print('Скачиваем перевод')
        vo_path = wget.download(vo_url, out=settings.TRANSLATOR_TEMP_PATH, bar=wget.bar_adaptive)
        print(vo_path)

        print('\nСкачиваем видео:')
        ydl_opts = {
            'noplaylist': True,
            'format': output_format.preset,
            'outtmpl': settings.TRANSLATOR_TEMP_PATH + '/%(title)s.%(ext)s',
            'concurrent-fragments': 3,
        }

        if output_format.postprocessors:
            ydl_opts['postprocessors'] = output_format.postprocessors

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                yinfo = ydl.extract_info(video_url, download=True)
            print(Style.DIM + Fore.GREEN + 'ВИДЕО СКАЧАНО' + Style.RESET_ALL)

            original_video_path = ydl.prepare_filename(yinfo)

            merge_video_and_vo(original_video_path, vo_path)

            print(Style.DIM + Fore.GREEN + '\nГОТОВО' + Style.RESET_ALL)
            print('Все операции успешно завершены. Можно скачать что-нибудь еще.')
        except yt_dlp.DownloadError:
            print(Style.DIM + Fore.RED + '\n\nYOU DIED' + Style.RESET_ALL)
            print('\nНе удалось скачать видео. Нам очень жаль. :('
                  '\nТак бывает, если оно еще не до конца обработалось на сервисе или вы ввели неправильную ссылку. '
                  'Попробуйте позже.')

        input('\nДля продолжения нажмите ENTER...')
        clear_console()


if __name__ == '__main__':
    main()
