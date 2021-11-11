from legacy_smg.preset import OutputFormat

output_formats = [
    OutputFormat(label='Аудио, m4a  (оптимально для YouTube)', preset='bestaudio[ext=m4a]/best',
                 postprocessors=[
                     {'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a', 'preferredquality': '128'},
                     {'key': 'FFmpegMetadata'}
                 ], type='audio'),
    OutputFormat(label='Видео, 1080p, mp4', preset='bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]',
                 postprocessors=[{'key': 'FFmpegMetadata'}]),
    OutputFormat(label='Видео, 1440, mp4', preset='bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/best[height<=1440]',
                 postprocessors=[{'key': 'FFmpegMetadata'}]),
    OutputFormat(label='Видео, 4K, mp4', preset='bestvideo[height<=4096][ext=mp4]+bestaudio[ext=m4a]/best[height<=4096]',
                 postprocessors=[{'key': 'FFmpegMetadata'}]),
    OutputFormat(label='Аудио в максимальном качестве (оптимально для Twitch)', preset='bestaudio/best',
                 postprocessors=[
                     {'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a', 'preferredquality': '192'},
                     {'key': 'FFmpegMetadata'}
                 ], type='audio'),
]