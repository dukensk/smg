@echo off
chcp 65001
cd %~dp0
cd ..
echo Создаем виртуальное окружение venv
python -m venv venv
echo. & echo Активируем его
call  venv\Scripts\activate.bat
echo. & echo Обновляем pip
call venv\Scripts\python.exe -m pip install --upgrade pip
echo. & echo Устанавливаем пакеты из requirements.txt
pip install --upgrade -r requirements.txt
call venv\Scripts\deactivate.bat
echo. & echo Готово
pause