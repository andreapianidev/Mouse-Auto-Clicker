@echo off
chcp 65001
echo.
echo ===================================================================
echo  Installazione Dipendenze per Mouse Auto Clicker su Windows
echo ===================================================================
echo.
echo Questo script installera tutte le dipendenze necessarie.

REM Imposta un mirror per pip per risolvere problemi di connessione
echo.
echo --- Fase 1: Configurazione del mirror per pip ---
echo Verra utilizzato un mirror pubblico per accelerare il download.
pip config set global.index-url https://pypi.org/simple/

REM Aggiorna pip
echo.
echo --- Fase 2: Aggiornamento di pip ---
python -m pip install --upgrade pip

REM Installa le dipendenze
echo.
echo --- Fase 3: Installazione delle dipendenze ---
pip install --timeout 120 -r requirements.txt

REM Installa singolarmente i pacchetti in caso di errore
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo Tentativo di installazione dei pacchetti singolarmente...
    pip install pyautogui
    pip install opencv-python
    pip install pillow
    pip install numpy
)

REM Verifica installazione
echo.
echo --- Fase 4: Verifica dell'installazione ---
python -c "import pyautogui; print('PyAutoGUI installato correttamente')" || echo "Errore: PyAutoGUI non trovato"
python -c "import cv2; print('OpenCV installato correttamente')" || echo "Errore: OpenCV (cv2) non trovato"
python -c "import PIL; print('Pillow installato correttamente')" || echo "Errore: Pillow (PIL) non trovato"
python -c "import numpy; print('NumPy installato correttamente')" || echo "Errore: NumPy non trovato"

echo.
echo ===================================================================
echo  Installazione Completata!
echo ===================================================================
echo.
echo Ora puoi eseguire il programma con il comando:
echo python mouse_clicker.py
echo.
echo Premere un tasto per uscire...
pause > nul