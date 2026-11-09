@echo off
rem Ders Kitabi Denetleyici arayuzunu baslatir. Tarayici kendiliginden acilir.
cd /d "%~dp0"

rem Streamlit ilk calistirmada e-posta adresi soruyor. Bos bir kimlik dosyasi
rem olusturarak bu soruyu atliyoruz (Streamlit'in kendisi de cevap verilince ayni dosyayi yazar).
if not exist "%USERPROFILE%\.streamlit\credentials.toml" (
    if not exist "%USERPROFILE%\.streamlit" mkdir "%USERPROFILE%\.streamlit"
    > "%USERPROFILE%\.streamlit\credentials.toml" (
        echo [general]
        echo email = ""
    )
)

if exist ".venv\Scripts\python.exe" (
    set PYTHON=".venv\Scripts\python.exe"
) else if exist "..\.venv\Scripts\python.exe" (
    set PYTHON="..\.venv\Scripts\python.exe"
) else (
    echo [HATA] Program kurulmamis. Once kurulum.bat dosyasina cift tiklayin.
    pause
    exit /b 1
)

echo Ders Kitabi Denetleyici baslatiliyor. Bu pencereyi program kullanildigi surece kapatmayin.
%PYTHON% -m streamlit run arayuz.py
pause
