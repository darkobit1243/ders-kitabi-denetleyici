@echo off
title Ders Kitabi Denetleyici
rem Programin arayuzunu baslatir; tarayici kendiliginden acilir.
cd /d "%~dp0uygulama"

rem Streamlit ilk calistirmada e-posta adresi soruyor. Bos bir kimlik dosyasi
rem olusturarak bu soruyu atliyoruz (Streamlit'in kendisi de cevap verilince ayni dosyayi yazar).
if not exist "%USERPROFILE%\.streamlit\credentials.toml" (
    if not exist "%USERPROFILE%\.streamlit" mkdir "%USERPROFILE%\.streamlit"
    > "%USERPROFILE%\.streamlit\credentials.toml" (
        echo [general]
        echo email = ""
    )
)

rem Gelistirme bilgisayarinda proje klasorunun disindaki sanal ortam da kullanilabilir
if exist ".venv\Scripts\python.exe" (
    set PYTHON=".venv\Scripts\python.exe"
) else if exist "..\..\.venv\Scripts\python.exe" (
    set PYTHON="..\..\.venv\Scripts\python.exe"
) else (
    echo [HATA] Program kurulmamis. Once KURULUM.bat dosyasina cift tiklayin.
    pause
    exit /b 1
)

echo ============================================================
echo   Ders Kitabi Denetleyici calisiyor.
echo   Tarayicida http://localhost:8501 adresi acilacak.
echo   Program kullanildigi surece bu pencereyi KAPATMAYIN.
echo   Kapatmak icin bu pencereyi kapatin.
echo   Teknik hata kayitlari: uygulama\hata_gunlugu.txt
echo ============================================================
%PYTHON% -m streamlit run arayuz.py 2> hata_gunlugu.txt
pause
