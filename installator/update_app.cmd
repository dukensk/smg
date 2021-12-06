@echo off
chcp 65001
cd %~dp0
cd ..

echo Обновляем приложение из Git-репозитория
git pull

echo. & echo Активируем виртуальное окружение
call  venv\Scripts\activate.bat

echo. & echo Обновляем pip
call venv\Scripts\python.exe -m pip install --upgrade pip

echo. & echo Обновляем пакеты из requirements.txt
pip install --upgrade -r requirements.txt

call venv\Scripts\deactivate.bat

echo. & echo Готово
pause