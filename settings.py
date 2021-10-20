from smg.preset import OutputFormat

SAVE_PATH = 'd:/Sort/Downloads/YouTube'
'''Путь для сохранения скачанных файлов'''

output_formats = [
    OutputFormat(label='Аудио, m4a  (оптимально для YouTube)', preset='bestaudio[ext=m4a]/best',
                 postprocessors=[{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a', 'preferredquality': '128'}]),
    OutputFormat(label='Видео, 1080p, webm', preset='bestvideo[height<=1080]+bestaudio/best[height<=1080]'),
    OutputFormat(label='Видео, 1440p, webm', preset='bestvideo[height<=1440]+bestaudio/best[height<=1440]'),
    OutputFormat(label='Видео, 4K, webm', preset='bestvideo[height<=4096]+bestaudio/best[height<=4096]'),
    OutputFormat(label='Видео, 1080p, mp4', preset='bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]'),
    OutputFormat(label='Видео, 720p', preset='bestvideo[height<=720]+bestaudio/best[height<=720]'),
    OutputFormat(label='Видео в максимальном качестве', preset='bestvideo+bestaudio/best'),
    OutputFormat(label='Аудио в максимальном качестве (оптимально для Twitch)', preset='bestaudio/best',
                 postprocessors=[{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a', 'preferredquality': '192'}]),
]
