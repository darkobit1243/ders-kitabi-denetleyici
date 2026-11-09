@echo off
chcp 65001 > nul
rem Ders Kitabi Denetleyici - kurulum
rem Proje klasorunde bir Python sanal ortami (.venv) olusturur ve gerekli paketleri kurar.
cd /d "%~dp0"

set PYTHON=
where py > nul 2>&1 && set PYTHON=py -3
if not defined PYTHON (
    where python > nul 2>&1 && set PYTHON=python
)
if not defined PYTHON (
    echo [HATA] Python bulunamadi. Lutfen Python 3.11 veya ustunu kurun: https://www.python.org
    echo Kurulumda "Add python.exe to PATH" secenegini isaretleyin.
    pause
    exit /b 1
)

%PYTHON% -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"
if errorlevel 1 (
    echo [HATA] Python 3.11 veya ustu gereklidir.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Sanal ortam olusturuluyor...
    %PYTHON% -m venv .venv || (echo [HATA] Sanal ortam olusturulamadi. & pause & exit /b 1)
)

if exist "paketler\" (
    echo Paketler "paketler" klasorunden kuruluyor ^(internet gerekmez^)...
    ".venv\Scripts\python.exe" -m pip install --no-index --find-links paketler -r requirements.txt
) else (
    echo Paketler internetten indirilip kuruluyor...
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
)
if errorlevel 1 (
    echo [HATA] Paketler kurulamadi.
    pause
    exit /b 1
)

echo.
echo Kurulum tamamlandi. Programi baslatmak icin baslat.bat dosyasina cift tiklayin.
pause
