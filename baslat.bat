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

if exist "..\.venv\Scripts\python.exe" (
    "..\.venv\Scripts\python.exe" -m streamlit run arayuz.py
) else if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -m streamlit run arayuz.py
) else (
    python -m streamlit run arayuz.py
)
pause
