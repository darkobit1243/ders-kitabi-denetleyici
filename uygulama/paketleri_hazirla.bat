@echo off
rem Internet baglantisi OLAN bir bilgisayarda calistirilir. Gerekli paketleri "paketler"
rem klasorune indirir. Bu klasorle birlikte kopyalanan program, internet baglantisi
rem OLMAYAN bilgisayarda kurulum.bat ile kurulabilir.
rem Not: Iki bilgisayarda Python surumu (or. 3.14) ve Windows mimarisi (64 bit) ayni olmalidir.
cd /d "%~dp0"
python -m pip download -r requirements.txt -d paketler
pause
