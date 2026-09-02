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


def extract_file_info(mediafile: MediaFile) -> dict:
    """Извлекает метаданные и главы из аудиофайла."""
    cmd = [
        'ffprobe',
        '-v',
        'quiet',
        '-print_format',
        'json',
        '-show_format',
        '-show_streams',
        '-show_chapters',
        str(mediafile.path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f'ffprobe failed: {result.stderr.strip()}')

    return json.loads(result.stdout)


def extract_tags(data: dict) -> dict[str, str]:
    """Собирает все метатеги из формата и аудио-потока."""
    tags = {}

    # Приоритет у тегов контейнера (format)
    if 'format' in data and 'tags' in data['format']:
        tags.update(data['format']['tags'])

    # Тегі аудио-потока добавляем, если отсутствуют
    for stream in data.get('streams', []):
        if stream.get('codec_type') == 'audio' and 'tags' in stream:
            for key, value in stream['tags'].items():
                if key not in tags:
                    tags[key] = value

    return tags


def build_chapters_list(chapters: list[dict]) -> str:
    """Формирует список глав в формате HH:MM:SS Title."""
    lines = []
    for i, chap in enumerate(chapters):
        start_ms = float(chap['start'])
        start_sec = start_ms / 1000.0

        # Первая глава всегда начинается с 00:00:00
        if i == 0 and start_sec > 0:i
            time_str = '00:00:00'
        else:
            time_str = format_time(start_sec)

        title = chap.get('tags', {}).get('title', 'Untitled')
        lines.append(f'{time_str} {title}')

    return '\n'.join(lines)


def prepare_metadata(mediafile: MediaFile) -> dict[str, str]:
    """Готовит финальный словарь метатегов для записи в файл."""
    data = extract_file_info(mediafile)
    tags = extract_tags(data)
    chapters = data.get('chapters', [])

    # Заменяем description главами, только если их >= 3
    if len(chapters) >= 3:
        tags['description'] = build_chapters_list(chapters)

    # Удаляем synopsis и comment
    tags.pop('synopsis', None)
    tags.pop('comment', None)

    return tags


def build_metadata_args(tags: dict[str, str]) -> list[str]:
    """Формирует список -metadata аргументов для FFmpeg."""
    args = []
    for key, value in tags.items():
        # FFmpeg понимает \n как перенос строки в значениях метаданных
        escaped = value.replace('\\', '\\\\').replace('"', '\\"')
        args.extend(['-metadata', f'{key}={escaped}'])
    return args


def copy_chapters_to_description(mediafile: MediaFile) -> None:
    """Копирует главы из секции Menu в метатег description."""
    input_path = mediafile.path
    output_path = mediafile.path.with_suffix('.opus.tmp')

    tags = prepare_metadata(mediafile)

    metadata_args = build_metadata_args(tags)

    cmd = [
        'ffmpeg',
        '-y',
        '-i', str(input_path),
        '-map_metadata', '-1',   # очистить оригинальные метаданные
        '-c', 'copy',
        *metadata_args,
        str(output_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f'ffmpeg failed: {result.stderr.strip()}')

    # Атомарная замена файла
    if input_path.exists():
        input_path.unlink()

    output_path.rename(input_path)
