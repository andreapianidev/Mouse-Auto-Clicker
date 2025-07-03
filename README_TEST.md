# Come Testare la Finestra di Licenza su macOS

Se hai già acquistato la licenza premium ma vuoi testare la finestra di licenza, puoi utilizzare gli script di test forniti.

## Opzioni di Test Disponibili

### 1. Test Completo con Reset Temporaneo (`test_license_reset.py`)

Questo script ti permette di testare completamente il sistema di licenze:

```bash
python3 test_license_reset.py
```

**Caratteristiche:**
- Interfaccia grafica completa
- Backup automatico dei tuoi dati di licenza
- Test con diversi scenari (4 utilizzi, 5 utilizzi, primo avvio)
- Ripristino automatico dei dati originali
- Visualizzazione dello stato attuale della licenza

**Scenari di Test:**
- **4 utilizzi**: Mostra l'avviso "1 utilizzo rimasto"
- **5 utilizzi**: Mostra la finestra di acquisto licenza premium
- **0 utilizzi**: Simula il primo avvio dell'applicazione

### 2. Test Semplice (`test_license_simple.py`)

Test rapido della finestra di licenza senza modificare i tuoi dati:

```bash
python3 test_license_simple.py
```

**Caratteristiche:**
- Test veloce senza interfaccia
- Non modifica i tuoi dati di licenza
- Mostra direttamente la finestra di licenza
- Output nel terminale

### 3. Test Dialog Originale (`test_license_dialog.py`)

Test della finestra di licenza con setup Tkinter base:

```bash
python3 test_license_dialog.py
```

## Istruzioni Dettagliate

### Per il Test Completo:

1. **Apri il Terminale** e naviga nella cartella del progetto:
   ```bash
   cd "/Users/andreapiani/CascadeProjects/autoclicker/Mouse Auto Clicker"
   ```

2. **Esegui lo script di test completo:**
   ```bash
   python3 test_license_reset.py
   ```

3. **Utilizza l'interfaccia:**
   - Clicca su "Test con 4 utilizzi" per vedere l'avviso di limite
   - Clicca su "Test con 5 utilizzi" per vedere la finestra di acquisto
   - Clicca su "Test primo avvio" per simulare il primo utilizzo
   - Usa "Mostra Stato Licenza Attuale" per vedere i tuoi dati reali

4. **I tuoi dati originali vengono automaticamente ripristinati** dopo ogni test

### Per il Test Rapido:

1. **Esegui direttamente:**
   ```bash
   python3 test_license_simple.py
   ```

2. **La finestra di licenza si aprirà immediatamente**

## Sicurezza dei Dati

✅ **I tuoi dati di licenza sono al sicuro:**
- Viene creato un backup automatico prima di ogni test
- I dati originali vengono sempre ripristinati
- Nessuna modifica permanente ai tuoi file di licenza

## Risoluzione Problemi

### Se lo script non si avvia:
```bash
# Verifica che Python3 sia installato
python3 --version

# Verifica che tkinter sia disponibile
python3 -c "import tkinter; print('Tkinter OK')"
```

### Se appare un errore di moduli:
```bash
# Assicurati di essere nella cartella corretta
pwd
# Dovrebbe mostrare: /Users/andreapiani/CascadeProjects/autoclicker/Mouse Auto Clicker
```

### Per ripristinare manualmente i dati:
Se qualcosa va storto, puoi sempre:
1. Aprire `test_license_reset.py`
2. Cliccare su "Ripristina Dati Originali"
3. Oppure eliminare il file `license_data.json` per resettare completamente

## Note Tecniche

- Gli script utilizzano le stesse classi dell'applicazione principale
- La finestra di licenza avrà lo stesso aspetto dell'applicazione reale
- Tutti i test sono compatibili con macOS e utilizzano font di sistema
- I backup vengono salvati come `license_data_backup.json`

## Esempi di Output

**Test con 4 utilizzi:**
```
Stato test:
Utilizzi: 4/5
Rimanenti: 1
Può usare app: True
```

**Test con 5 utilizzi:**
```
Stato test:
Utilizzi: 5/5
Rimanenti: 0
Può usare app: False
→ Mostra finestra acquisto licenza
```

Ora puoi testare facilmente la finestra di licenza su macOS! 🎉