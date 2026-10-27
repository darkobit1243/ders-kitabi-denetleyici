@echo off
rem Ders Kitabi Denetleyici arayuzunu baslatir. Tarayici kendiliginden acilir.
cd /d "%~dp0"
if exist "..\.venv\Scripts\python.exe" (
    "..\.venv\Scripts\python.exe" -m streamlit run arayuz.py
) else if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -m streamlit run arayuz.py
) else (
    python -m streamlit run arayuz.py
)
pause
