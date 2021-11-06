import subprocess
import os
import pathlib

from colorama import Fore, Style

import settings


def show_app_header():
    """Выводит заголовок приложения"""
    print('SMG: Translator by Duke\n')


def extract_original_audio(original_video_path: str) -> str:
    """
    Извлекаем оригинальное аудио
    :param original_video_path: абсолютный путь к оригинальному видео
    :return: абсолютный путь к извлеченному аудио
    """
    print('\nИзвлекаем оригинальное аудио...')
    path = pathlib.Path(original_video_path)
    filename = path.stem
    output_ext = "m4a"
    output_file_path = '{save_path}/{filename}_en.{ext}' \
        .format(save_path=settings.TRANSLATOR_TEMP_PATH, filename=filename, ext=output_ext)
    subprocess.call(['ffmpeg',
                     '-i', original_video_path,
                     '-vn',
                     '-acodec', 'copy',
                     output_file_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)

    print(Style.DIM + Fore.GREEN + 'АУДИО ИЗВЛЕЧЕНО' + Style.RESET_ALL);
    return output_file_path


def resample_vo(vo_audio_path: str) -> str:
    print('\nРеcемплируем закадровый перевод...')
    path = pathlib.Path(vo_audio_path)
    filename = path.stem
    output_ext = "m4a"
    output_file_path = '{save_path}/{filename}_resampled.{ext}' \
        .format(save_path=settings.TRANSLATOR_TEMP_PATH, filename=filename, ext=output_ext)

    subprocess.call(['ffmpeg',
                     '-i', vo_audio_path,
                     '-ar', '44100',
                     '-ab', settings.TRANSLATOR_OUTPUT_AUDIO_BITRATE,
                     output_file_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)

    print(Style.DIM + Fore.GREEN + 'ГОТОВО' + Style.RESET_ALL)
    return output_file_path


def muffle_audio(original_audio_path: str) -> str:
    print('\nПриглушаем оригинальное аудио...')
    path = pathlib.Path(original_audio_path)
    filename = path.stem
    output_ext = "m4a"
    output_file_path = '{save_path}/{filename}_muffled.{ext}' \
        .format(save_path=settings.TRANSLATOR_TEMP_PATH, filename=filename, ext=output_ext)

    subprocess.call(['ffmpeg',
                     '-i', original_audio_path,
                     '-af', 'volume=' + str(settings.TRANSLATOR_VOLUME_ORIGINAL_AUDIO),
                     output_file_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)

    print(Style.DIM + Fore.GREEN + 'ПРИГЛУШИЛИ НА '
          + str(round((1 - settings.TRANSLATOR_VOLUME_ORIGINAL_AUDIO) * 100)) + '%' + Style.RESET_ALL)
    return output_file_path


def merge_audio(original_video_path: str, vo_path: str, muffled_audio_path: str):
    print('\nНакладываем закадровый перевод...')
    path = pathlib.Path(original_video_path)
    filename = path.stem
    output_ext = "m4a"
    output_file_path = '{save_path}/{filename}_merged.{ext}' \
        .format(save_path=settings.TRANSLATOR_TEMP_PATH, filename=filename, ext=output_ext)

    subprocess.call(['ffmpeg',
                     '-i', vo_path,
                     '-i', muffled_audio_path,
                     '-filter_complex', 'amix=inputs=2:duration=first',
                     '-ab', settings.TRANSLATOR_OUTPUT_AUDIO_BITRATE,
                     output_file_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT
                    )

    print(Style.DIM + Fore.GREEN + 'ГОТОВО' + Style.RESET_ALL)
    return output_file_path


def replace_audio_in_video(original_video_path: str, new_audio_path: str):
    print('\nЗаменяем аудио в исходном видео...')
    path = pathlib.Path(original_video_path)
    filename = path.stem
    output_ext = "mp4"
    output_file_path = '{save_path}/{filename}.{ext}' \
        .format(save_path=settings.TRANSLATOR_SAVE_PATH, filename=filename, ext=output_ext)

    subprocess.call(['ffmpeg',
                     '-i', original_video_path,
                     '-i', new_audio_path,
                     '-c', 'copy',
                     '-map', '0:v:0',
                     '-map', '1:a:0',
                     output_file_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT
                    )

    print(Style.DIM + Fore.GREEN + 'ВИДЕО ПЕРЕВЕДЕНО' + Style.RESET_ALL)
    return output_file_path


def remove_temp_files(temp_files):
    """Удаляем временные файлы"""
    for file_path in temp_files:
        os.remove(file_path)


def merge_audio_only(original_audio_path: str, vo_path: str, muffled_audio_path: str):
    print('\nНакладываем закадровый перевод...')
    path = pathlib.Path(original_audio_path)
    filename = path.stem
    output_ext = "m4a"
    output_file_path = '{save_path}/{filename}.{ext}' \
        .format(save_path=settings.TRANSLATOR_SAVE_PATH, filename=filename, ext=output_ext)

    subprocess.call(['ffmpeg',
                     '-i', vo_path,
                     '-i', muffled_audio_path,
                     '-filter_complex', 'amix=inputs=2:duration=first',
                     '-ab', settings.TRANSLATOR_OUTPUT_AUDIO_BITRATE,
                     output_file_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT
                    )

    print(Style.DIM + Fore.GREEN + 'ГОТОВО' + Style.RESET_ALL)
    return output_file_path


def merge_video_and_vo(original_video_path: str, vo_audio_path: str):
    temp_files = [original_video_path, vo_audio_path]

    original_audio_path = extract_original_audio(original_video_path)
    temp_files.append(original_audio_path)

    muffled_audio_path = muffle_audio(original_audio_path)
    temp_files.append(muffled_audio_path)

    resampled_vo_path = resample_vo(vo_audio_path)
    temp_files.append(resampled_vo_path)

    merged_audio_path = merge_audio(original_video_path, resampled_vo_path, muffled_audio_path)
    temp_files.append(merged_audio_path)

    output_video_path = replace_audio_in_video(original_video_path, merged_audio_path)

    print('Переведенный файл: ' + output_video_path)
    remove_temp_files(temp_files)


def merge_audio_and_vo(original_audio_path: str, vo_audio_path: str):
    temp_files = [original_audio_path, vo_audio_path]

    muffled_audio_path = muffle_audio(original_audio_path)
    temp_files.append(muffled_audio_path)

    resampled_vo_path = resample_vo(vo_audio_path)
    temp_files.append(resampled_vo_path)

    output_audio_path = merge_audio_only(original_audio_path, resampled_vo_path, muffled_audio_path)
    print('Переведенный файл: ' + output_audio_path)
    remove_temp_files(temp_files)
