#!/bin/bash

cd "$(dirname "$(readlink -f "$0")")"
cd ..

echo 'Обновляем приложение из Git-репозитория'
git pull

echo  -e '\nОбновляем пакеты'
uv sync

echo  -e '\nГотово'
