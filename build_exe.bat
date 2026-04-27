@echo off
echo ============================================
echo   Wilma Kurssivalitsin -- EXE-paketoija
echo ============================================
echo.

:: Tarkistetaan onko Python asennettu
python --version >nul 2>&1
if errorlevel 1 (
    echo VIRHE: Pythonia ei loydy!
    echo Lataa Python osoitteesta: https://www.python.org/downloads/
    echo Muista valita "Add Python to PATH" asennuksen aikana.
    pause
    exit /b 1
)

echo [1/3] Asennetaan tarvittavat kirjastot...
python -m pip install selenium pyinstaller --quiet
if errorlevel 1 (
    echo VIRHE: Kirjastojen asennus epaonnistui!
    pause
    exit /b 1
)

echo [2/3] Paketoidaan EXE-tiedostoksi...
python -m PyInstaller --onefile --windowed --name "WilmaKurssivalitsin" wilma_valitsin.py
if errorlevel 1 (
    echo VIRHE: Paketointi epaonnistui!
    pause
    exit /b 1
)

echo [3/3] Valmis!
echo.
echo EXE-tiedosto loytyy kansiosta: dist\WilmaKurssivalitsin.exe
echo.
echo Jaa kaverillesi vain tama yksi tiedosto!
echo (Google Chrome taytyy olla asennettuna kohdekoneella)
echo.
pause
