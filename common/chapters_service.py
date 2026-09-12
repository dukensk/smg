import json
import subprocess

from mutagen.oggopus import OggOpus

from common.media import MediaFile, is_audio_file


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

    result = subprocess.run(cmd, capture_output=True, text=True, errors='replace')
    if result.returncode != 0:
        raise RuntimeError(f'ffprobe failed: {result.stderr.strip()}')

    return json.loads(result.stdout)


def extract_tags(data: dict) -> dict[str, str]:
    """Собирает все метатеги из формата и аудио-потока."""
    tags = {}

    # Приоритет у тегов контейнера (format)
    if 'format' in data and 'tags' in data['format']:
        tags.update(data['format']['tags'])

    # Теги аудио-потока добавляем, если отсутствуют
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
        # ffprobe обычно использует 'start_time' в секундах.
        start_sec = float(chap.get('start_time', chap.get('start', 0)))

        # Первая глава всегда начинается с 00:00:00
        if i == 0 and start_sec > 0:
            time_str = '00:00:00'
        else:
            time_str = format_time(start_sec)

        title = chap.get('tags', {}).get('title', 'Untitled')
        lines.append(f'{time_str} {title}')

    return '\n'.join(lines)


def prepare_metadata(mediafile: MediaFile) -> tuple[dict[str, str], str]:
    """Готовит финальный словарь метатегов и формат файла."""
    data = extract_file_info(mediafile)
    tags = extract_tags(data)
    chapters = data.get('chapters', [])
    # Получаем format_name из данных ffprobe (например, 'ogg')
    fmt = data.get('format', {}).get('format_name', 'ogg')

    # Заменяем description главами, только если их >= 3
    if len(chapters) >= 3:
        tags['description'] = build_chapters_list(chapters)

    # Удаляем synopsis и comment
    tags.pop('synopsis', None)
    tags.pop('comment', None)

    return tags, fmt


def build_metadata_args(tags: dict[str, str]) -> list[str]:
    """Формирует список -metadata аргументов для FFmpeg."""
    args = []
    for key, value in tags.items():
        # FFmpeg понимает \n как перенос строки в значениях метаданных
        escaped = str(value).replace('\\', '\\\\').replace('"', '\\"')
        args.extend(['-metadata', f'{key}={escaped}'])
    return args


def copy_chapters_to_description(mediafile: MediaFile) -> None:
    """Копирует главы из секции Menu в метатег description."""
    input_path = mediafile.path
    # Создаем временный файл с расширением, отличным от оригинала
    output_path = input_path.with_suffix(input_path.suffix + '.tmp')

    tags, fmt = prepare_metadata(mediafile)
    metadata_args = build_metadata_args(tags)

    cmd = [
        'ffmpeg',
        '-y',
        '-i', str(input_path),
        '-map_metadata', '-1',   # очистить оригинальные метаданные
        '-c', 'copy',
        '-f', fmt,              # Явно указываем формат (исправляет вашу ошибку)
        *metadata_args,
        str(output_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, errors='replace')
    if result.returncode != 0:
        raise RuntimeError(f'ffmpeg failed: {result.stderr.strip()}')

    # Атомарная замена файла
    if input_path.exists():
        input_path.unlink()

    output_path.rename(input_path)



def get_chapter_tags(mediafile: MediaFile):
    """Извлекает теги глав из медиафайла"""
    source = OggOpus(mediafile.path)
    # Извлекаем только теги глав (регистронезависимо)
    # Исправлено: добавлены .items() и обработка None через or {}
    chapters_tags = {
        key: value
        for key, value in (source.tags or {}).items()
        if key.upper().startswith('CHAPTER')
    }

    if not chapters_tags:
        chapters_tags = {}

    return chapters_tags


def add_chapters(mediafile: MediaFile, chapters_tags: dict):
    """Добавляет главы из chapters_tags в теги медиафайла"""
    if not chapters_tags:
        return

    target = OggOpus(mediafile.path)
    for key, value in chapters_tags.items():
        target.tags[key] = value

    target.save()


def chapters_postprocess(mediafile: MediaFile) -> MediaFile:
    """Постобработка глав в медиафайле"""
    if is_audio_file(mediafile):
        chapters_tags = get_chapter_tags(mediafile)
        copy_chapters_to_description(mediafile)
        add_chapters(mediafile, chapters_tags)

    return mediafile
