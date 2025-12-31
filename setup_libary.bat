@echo off
chcp 65001 >nul
title Edge Utility Pro - Установка и запуск
color 0E
cls

echo ════════════════════════════════════════════════
echo    Edge Utility Pro - Установка и запуск
echo ════════════════════════════════════════════════
echo.

:: Проверка прав администратора
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [✓] Запуск с правами администратора
) else (
    echo [!] Для установки рекомендуется запустить от имени администратора
    echo.
    set /p admin="Запустить от имени администратора? (Y/N): "
    if /i "%admin%"=="Y" (
        powershell -Command "Start-Process '%~f0' -Verb RunAs"
        exit
    )
)

:MAIN_MENU
cls
echo ════════════════════════════════════════════════
echo          Edge Utility Pro v4.0
echo ════════════════════════════════════════════════
echo.
echo 1. Проверить и установить Python
echo 2. Установить необходимые библиотеки
echo 3. Запустить программу
echo 4. Установить всё автоматически
echo 5. Выход
echo.
set /p choice="Выберите действие (1-5): "

if "%choice%"=="1" goto CHECK_PYTHON
if "%choice%"=="2" goto INSTALL_LIBS
if "%choice%"=="3" goto RUN_PROGRAM
if "%choice%"=="4" goto AUTO_INSTALL
if "%choice%"=="5" goto EXIT
goto MAIN_MENU

:CHECK_PYTHON
cls
echo Проверка установки Python...
echo.
python --version >nul 2>&1
if %errorLevel% == 0 (
    python --version
    echo [✓] Python уже установлен
    pause
    goto MAIN_MENU
) else (
    echo [!] Python не найден
    echo.
    echo Скачивание Python 3.11...
    echo.
    
    :: Скачивание Python установщика
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python_installer.exe'"
    
    if exist python_installer.exe (
        echo [✓] Установщик скачан
        echo.
        echo Установка Python...
        echo ВАЖНО: Отметьте галочку "Add Python to PATH"!
        echo.
        start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        del python_installer.exe
        
        :: Обновление переменных среды
        setx PATH "%PATH%;C:\Python311;C:\Python311\Scripts"
        
        echo [✓] Python установлен
        echo Перезапустите командную строку или систему
    ) else (
        echo [!] Ошибка скачивания Python
        echo Установите Python вручную с https://python.org
    )
    pause
    goto MAIN_MENU
)

:INSTALL_LIBS
cls
echo Установка необходимых библиотек...
echo.
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Python не установлен!
    pause
    goto MAIN_MENU
)

echo Установка библиотек через pip...
echo.

:: Обновление pip
echo [1/8] Обновление pip...
python -m pip install --upgrade pip --quiet
if %errorLevel% == 0 echo [✓] pip обновлен

:: Основные библиотеки
echo [2/8] Установка colorama...
python -m pip install colorama --quiet
if %errorLevel% == 0 echo [✓] colorama установлен

echo [3/8] Установка pyperclip...
python -m pip install pyperclip --quiet
if %errorLevel% == 0 echo [✓] pyperclip установлен

echo [4/8] Установка qrcode...
python -m pip install qrcode[pil] --quiet
if %errorLevel% == 0 echo [✓] qrcode установлен

echo [5/8] Установка requests...
python -m pip install requests --quiet
if %errorLevel% == 0 echo [✓] requests установлен

echo [6/8] Установка psutil...
python -m pip install psutil --quiet
if %errorLevel% == 0 echo [✓] psutil установлен

:: Дополнительные библиотеки
echo [7/8] Установка py-cpuinfo...
python -m pip install py-cpuinfo --quiet
if %errorLevel% == 0 echo [✓] py-cpuinfo установлен

echo [8/8] Проверка установки...
python -c "import colorama, pyperclip, qrcode, requests, psutil, cpuinfo; print('[✓] Все библиотеки установлены')" 2>nul
if %errorLevel% neq 0 (
    echo [!] Некоторые библиотеки не установились
    echo Попробуйте установить их вручную:
    echo pip install colorama pyperclip qrcode[pil] requests psutil py-cpuinfo
)

echo.
echo [✓] Установка библиотек завершена
pause
goto MAIN_MENU

:RUN_PROGRAM
cls
echo Запуск Edge Utility Pro...
echo.
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Python не установлен!
    pause
    goto MAIN_MENU
)

:: Проверка наличия файла программы
if not exist "edge_utility.py" (
    echo [!] Файл edge_utility.py не найден!
    echo Убедитесь, что файл находится в той же папке
    pause
    goto MAIN_MENU
)

echo [✓] Python обнаружен
echo [✓] Запуск программы...
echo.
python edge_utility.py
pause
goto MAIN_MENU

:AUTO_INSTALL
cls
echo Автоматическая установка всего необходимого...
echo Эта операция может занять несколько минут...
echo.
timeout /t 3 /nobreak >nul

:: Проверка Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [1/3] Установка Python...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python_installer.exe'"
    if exist python_installer.exe (
        start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        del python_installer.exe
        echo [✓] Python установлен
    )
) else (
    echo [✓] Python уже установлен
)

:: Обновление pip
echo [2/3] Установка библиотек...
python -m pip install --upgrade pip --quiet
python -m pip install colorama pyperclip qrcode[pil] requests psutil py-cpuinfo --quiet

:: Проверка установки
python -c "import colorama, pyperclip, qrcode, requests, psutil" 2>nul
if %errorLevel% == 0 (
    echo [✓] Все библиотеки установлены
) else (
    echo [!] Были ошибки при установке
)

:: Запуск программы
echo [3/3] Запуск программы...
echo.
if exist "edge_utility.py" (
    python edge_utility.py
) else (
    echo [!] Файл edge_utility.py не найден!
    echo Поместите файл программы в эту папку
)
pause
goto MAIN_MENU

:EXIT
cls
echo Спасибо за использование Edge Utility Pro!
echo.
echo Автор: Edge Development Team
echo Версия: 4.0
echo.
timeout /t 3 /nobreak >nul
exit