@echo off
title Ders Kitabi Denetleyici - Kurulum
rem Programi bu bilgisayara kurar:
rem   1. uygulama\.venv klasorunde bir Python sanal ortami olusturur (bilgisayardaki diger programlar etkilenmez)
rem   2. Gerekli paketleri kurar (uygulama\paketler klasoru varsa internetsiz)
rem   3. Masaustu ve Baslat menusune kisayol ekler
cd /d "%~dp0uygulama"

echo ============================================================
echo   Ders Kitabi Denetleyici 1.0.0 - Kurulum
echo ============================================================
echo.

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

echo [1/3] Sanal ortam hazirlaniyor...
if not exist ".venv\Scripts\python.exe" (
    %PYTHON% -m venv .venv || (echo [HATA] Sanal ortam olusturulamadi. & pause & exit /b 1)
)

echo [2/3] Paketler kuruluyor, bu islem birkac dakika surebilir...
if exist "paketler\" (
    ".venv\Scripts\python.exe" -m pip install --disable-pip-version-check --no-index --find-links paketler -r requirements.txt
) else (
    ".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r requirements.txt
)
if errorlevel 1 (
    echo [HATA] Paketler kurulamadi. Internet baglantisini kontrol edin veya cevrimdisi kurulum icin README dosyasina bakin.
    pause
    exit /b 1
)

echo [3/3] Kisayollar olusturuluyor...
powershell -NoProfile -ExecutionPolicy Bypass -File "kisayol.ps1"

echo.
echo ============================================================
echo   Kurulum tamamlandi.
echo   Programi masaustundeki "Ders Kitabi Denetleyici" simgesiyle
echo   veya bu klasordeki BASLAT.bat dosyasiyla acabilirsiniz.
echo ============================================================
pause
