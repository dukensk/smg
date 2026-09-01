import json
import subprocess

from common.media import MediaFile


def format_time(seconds: float) -> str:
    """Преобразует секунды в формат HH:MM:SS."""
    total_seconds = int(round(seconds))
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    return f'{hours:02}:{minutes:02}:{secs:02}'


def get_all_metadata(mediafile: MediaFile) -> list[str]:
    """Извлекает все метаданные и формирует список глав для Description."""
    cmd = [
        'ffprobe',
        '-v',
        'quiet',
        '-print_format',
        'json',
        '-show_format',
        '-show_streams',
        '-show_chapters',  # Важно: извлекаем главы (Menu)
        str(mediafile.path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return []

    data = json.loads(result.stdout)
    tags = {}

    # 1. Собираем все существующие теги в словарь
    if 'format' in data and 'tags' in data['format']:
        tags.update(data['format']['tags'])

    for stream in data.get('streams', []):
        if stream.get('codec_type') == 'audio' and 'tags' in stream:
            # Добавляем теги потока, если их еще нет в словаре (приоритет формату)
            for k, v in stream['tags'].items():
                if k not in tags:
                    tags[k] = v

    # 2. Обработка глав (Menu)
    chapters = data.get('chapters', [])
    if len(chapters) >= 3:
        chapter_lines = []
        for i, chap in enumerate(chapters):
            start_time_ms = float(chap['start'])
            start_time_sec = start_time_ms / 1000.0

            # Правило: Первая глава должна начинаться строго с 00:00:00
            if i == 0 and start_time_sec > 0:
                time_str = '00:00:00'
            else:
                time_str = format_time(start_time_sec)

            title = chap.get('tags', {}).get('title', 'Untitled')
            chapter_lines.append(f'{time_str} {title}')

        # Заменяем или добавляем Description списком глав
        tags['description'] = '\n'.join(chapter_lines)

    tags.pop('synopsis', None)
    tags.pop('comment', None)

    # 3. Преобразуем словарь в список аргументов для FFmpeg
    metadata_args = []
    for key, value in tags.items():
        metadata_args.extend(['-metadata', f'{key}={value}'])
    return metadata_args


def copy_chapters_to_description(mediafile: MediaFile) -> None:
    """Копирует главы из файла в метатег описание"""
    original_file_path = mediafile.path
    output_file_path = original_file_path.with_suffix('.ogg')

    metadata_args = get_all_metadata(mediafile)

    subprocess.call(['ffmpeg',
                         '-i', original_file_path,
                         '-c', 'copy',               # Копируем поток без перекодирования
                         *metadata_args,              # Применяем все извлеченные теги
                         output_file_path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)

    if original_file_path.exists():
        original_file_path.unlink()

    if output_file_path.exists():
        output_file_path.rename(original_file_path)
