@echo off
title Ders Kitabi Denetleyici - Kaldirma
rem Kisayollari ve kurulan paketleri (uygulama\.venv) siler. Ornek kitaplar ve kod dosyalari silinmez.
cd /d "%~dp0"
echo Kisayollar ve kurulan paketler silinecek. Devam etmek icin bir tusa basin, iptal icin pencereyi kapatin.
pause > nul
powershell -NoProfile -ExecutionPolicy Bypass -File "kisayol.ps1" -Kaldir
if exist ".venv\" rmdir /s /q ".venv"
if exist ".onbellek\" rmdir /s /q ".onbellek"
if exist ".yuklenenler\" rmdir /s /q ".yuklenenler"
echo Kaldirma tamamlandi. Program klasorunu artik silebilirsiniz.
pause
