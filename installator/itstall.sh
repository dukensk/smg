#!/bin/bash

echo 'Устанавливаем SMG'

# Создаем директорию, если её нет
mkdir -p ~/.local/bin

echo 'Создаем симлинки'
ln -s ../scripts/smg.sh ~/.local/bin/smg
ln -s ../scripts/mediagrabber.sh ~/.local/bin/mediagrabber
ln -s ../scripts/translator.sh ~/.local/bin/translator


echo 'Делаем скрипт исполняемым'
chmod +x ../scripts/smg.sh
chmod +x ../scripts/smg.sh
chmod +x ../scripts/smg.sh

# Добавляем ~/.local/bin в PATH (если ещё не добавлен)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # или ~/.zshrc

# Применяем изменения
source ~/.bashrc  # или source ~/.zshrc

echo 'Готово'