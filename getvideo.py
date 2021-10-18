import sys
import yt_dlp

import settings

# Принудительно переключаем кодировку вывода консоли в UTF-8, чтобы не было проблем с кириллицей
sys.stdout.reconfigure(encoding='utf-8')

print('SMG by Duke. Скачивание видео')
video_url = input('Введите URL видео: ')

ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
    'outtmpl': settings.SAVE_PATH + '/%(title)s.%(ext)s',
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

input('\nНажмите ENTER')
