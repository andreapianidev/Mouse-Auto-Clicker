# Guida all'installazione per Windows

## Problema di connessione

Se stai riscontrando errori come questo durante l'installazione:

```
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.HTTPSConnection object at 0x0000021890DB3290>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed')': /simple/pyautogui/
```

Significa che hai problemi di connessione al Python Package Index (PyPI) o che un firewall sta bloccando le connessioni.

## Soluzione rapida

1. **Usa lo script di installazione automatico**
   - Fai doppio clic sul file `install_windows.bat` incluso in questa cartella
   - Lo script installerà tutte le dipendenze necessarie una per una

## Installazione manuale (alternativa)

Se lo script automatico non funziona, puoi installare manualmente le dipendenze:

1. **Aggiorna pip**:
   ```
   python -m pip install --upgrade pip
   ```

2. **Installa le dipendenze una per una**:
   ```
   pip install pillow
   pip install numpy
   pip install opencv-python
   pip install pyautogui
   ```

3. **Usa un mirror alternativo** se continui ad avere problemi di connessione:
   ```
   pip install pyautogui --index-url https://pypi.org/simple/
   ```

## Verifica dell'installazione

Per verificare che tutto sia installato correttamente, esegui:

```
python -c "import pyautogui; print('PyAutoGUI installato correttamente:', pyautogui.__version__)"
```

## Esecuzione del programma

Dopo l'installazione, puoi avviare il programma con:

```
python mouse_clicker.py
```

## Problemi comuni

- **Errore "tkinter not found"**: Installa tkinter con `pip install tk`
- **Errore con PyAutoGUI**: Assicurati di avere installato tutte le dipendenze (pillow, numpy, opencv-python)
- **Problemi di permessi**: Esegui il prompt dei comandi come amministratore

## Contatti

Se continui ad avere problemi, contatta il supporto tecnico.