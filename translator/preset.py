from smg.preset import OutputFormat

output_formats = [
    OutputFormat(label='Аудио, m4a  (оптимально для YouTube)', preset='bestaudio[ext=m4a]/best',
                 postprocessors=[{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a', 'preferredquality': '128'}]),
    OutputFormat(label='Видео, 1080p, mp4', preset='bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]'),
    OutputFormat(label='Видео, 1440, mp4', preset='bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/best[height<=1440]'),
    OutputFormat(label='Видео, 4K, mp4', preset='bestvideo[height<=4096][ext=mp4]+bestaudio[ext=m4a]/best[height<=4096]'),
    OutputFormat(label='Аудио в максимальном качестве (оптимально для Twitch)', preset='bestaudio/best',
                 postprocessors=[{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a', 'preferredquality': '192'}]),
]