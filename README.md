# 🖱️ Mouse Auto Clicker - Applicazione per Click Automatici

**Autore:** Andrea Piani  
**Versione:** 2.0.0  
**Linguaggio:** Python 3.7+

Un'applicazione desktop Python con interfaccia grafica intuitiva che simula click automatici del mouse a intervalli casuali. Perfetta per automazioni semplici e test di interfacce utente.

## 🚀 Caratteristiche Principali

- 🎯 **Interfaccia Intuitiva**: GUI semplice e funzionale realizzata con tkinter
- ⏱️ **Intervalli Personalizzabili**: Configura tempi minimi e massimi tra i click
- 🎮 **Controllo Completo**: Pulsanti dedicati per avviare e fermare l'automazione
- 📊 **Log Dettagliato**: Registro completo con timestamp e posizioni dei click
- 🎯 **Click Precisi**: Esecuzione nella posizione corrente del cursore
- 🎲 **Casualità**: Intervalli randomici per simulare comportamento umano
- 🛡️ **Sicurezza**: Sistema failsafe integrato per interruzioni d'emergenza
- 📦 **Portabilità**: Facilmente compilabile in eseguibile .exe per Windows

## 📸 Screenshot

![Mouse Auto Clicker Interface](https://www.andreapiani.com/autoclicker1.png)

*Interfaccia principale dell'applicazione con tutte le opzioni di configurazione*

## 📋 Requisiti di Sistema

| Componente | Versione | Note |
|------------|----------|------|
| **Python** | 3.7+ | Versione consigliata: 3.9+ |
| **tkinter** | Incluso | Libreria GUI standard Python |
| **pyautogui** | ≥0.9.54 | Per il controllo del mouse |

### Sistemi Operativi Supportati
- 🪟 **Windows** 10/11
- 🍎 **macOS** 10.14+
- 🐧 **Linux** (Ubuntu 18.04+, Debian 10+)

## 🛠️ Installazione

### Metodo 1: Clone da GitHub
```bash
# Clona il repository
git clone https://github.com/andreapiani/mouse-auto-clicker.git
cd mouse-auto-clicker

# Installa le dipendenze
pip install -r requirements.txt
```

### Metodo 2: Download diretto
1. Scarica il progetto come ZIP
2. Estrai i file in una cartella
3. Apri il terminale nella cartella del progetto
4. Esegui: `pip install -r requirements.txt`

## 🎯 Guida all'Uso

### Avvio Rapido
```bash
python mouse_clicker.py
```

### Configurazione
1. **Imposta Intervalli**
   - 🕐 **Minimo**: Tempo minimo tra i click (es. 1.0 secondi)
   - 🕕 **Massimo**: Tempo massimo tra i click (es. 5.0 secondi)

2. **Posizionamento**
   - Sposta il cursore nella posizione desiderata
   - I click avverranno esattamente in quella posizione

3. **Controllo**
   - ▶️ **Avvia**: Inizia la sequenza di click automatici
   - ⏹️ **Ferma**: Interrompe immediatamente l'automazione

### 🔥 Suggerimenti Pro
- Usa intervalli più lunghi per automazioni discrete
- Monitora il log per verificare l'attività
- Testa sempre con intervalli brevi prima dell'uso finale

## 🛡️ Sicurezza e Controlli

### Sistema Failsafe
- 🚨 **Emergenza**: Sposta rapidamente il mouse nell'**angolo superiore sinistro** per stop immediato
- 📊 **Monitoraggio**: Stato dell'applicazione sempre visibile
- 📝 **Tracciabilità**: Log completo di tutti i click con timestamp precisi

### Best Practices
- ✅ Testa sempre con intervalli brevi
- ✅ Verifica la posizione del cursore prima di avviare
- ✅ Mantieni il controllo dell'applicazione
- ❌ Non utilizzare per violare ToS di servizi online

## 📦 Compilazione Eseguibile

### Metodo Automatico (Consigliato)
```bash
python build_exe.py
```
Lo script automatico gestisce tutto il processo di compilazione!

### Metodo Manuale
```bash
# Installa pyinstaller
pip install pyinstaller

# Compila l'applicazione
pyinstaller --onefile --windowed --name="MouseAutoClicker" mouse_clicker.py
```

### 🎨 Opzioni Avanzate
```bash
# Con icona personalizzata
pyinstaller --onefile --windowed --icon=icon.ico --name="MouseAutoClicker" mouse_clicker.py

# Versione ottimizzata
pyinstaller --onefile --windowed --optimize=2 --name="MouseAutoClicker" mouse_clicker.py
```

**📁 Output**: Il file `.exe` sarà disponibile nella cartella `dist/`

## 📁 Struttura del Progetto

```
mouse-auto-clicker/
├── 🐍 mouse_clicker.py    # Applicazione principale
├── 📦 requirements.txt    # Dipendenze Python
├── 🔧 build_exe.py        # Script di compilazione automatica
└── 📖 README.md           # Documentazione del progetto
```

## 🎛️ Interfaccia Utente

### 🎮 Controlli Principali
| Elemento | Funzione | Dettagli |
|----------|----------|----------|
| **Spinbox Intervalli** | Imposta min/max secondi | Valori decimali supportati |
| **Pulsante Avvia** | Inizia automazione | Disabilitato durante l'esecuzione |
| **Pulsante Ferma** | Interrompe click | Stop immediato e sicuro |
| **Indicatore Stato** | Mostra stato corrente | Aggiornamento in tempo reale |

### 📊 Sistema di Log
- 🕐 **Timestamp**: Data e ora precisi per ogni click
- 📍 **Posizione**: Coordinate X,Y del click
- ⏱️ **Tempo Attesa**: Intervallo generato casualmente
- 🧹 **Pulizia**: Pulsante per svuotare il log
- 📜 **Scroll**: Area scrollabile per log lunghi

### ℹ️ Pannello Informazioni
- 📋 Istruzioni d'uso integrate nell'interfaccia
- 🛡️ Promemoria per la sicurezza
- 💡 Suggerimenti per l'utilizzo ottimale

## 🔧 Risoluzione Problemi

### ❌ Errori Comuni

#### "pyautogui non installato"
```bash
pip install pyautogui
# oppure
pip install -r requirements.txt
```

#### 🍎 macOS: Permessi di Accessibilità
1. **Preferenze di Sistema** → **Sicurezza e Privacy** → **Privacy**
2. Seleziona **"Accessibilità"** nella barra laterale
3. Clicca il lucchetto e inserisci la password
4. Aggiungi **Python** o **Terminale** alla lista
5. Riavvia l'applicazione

#### 🐧 Linux: Dipendenze Sistema
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-tk python3-dev

# Dipendenze pyautogui
sudo apt-get install scrot python3-pil python3-pil.imagetk

# Fedora/CentOS
sudo dnf install python3-tkinter python3-devel
```

#### 🪟 Windows: Problemi di Compilazione
- Assicurati di avere **Visual Studio Build Tools** installato
- Usa **Python dal Microsoft Store** per evitare problemi di permessi
- Esegui il terminale come **Amministratore** se necessario

## 🚧 Roadmap e Miglioramenti Futuri

### 🎯 Prossime Versioni
- [ ] 🔄 **System Tray**: Minimizzazione nell'area di notifica
- [ ] 📍 **Coordinate Fisse**: Click in posizioni predefinite
- [ ] 🚀 **Avvio Automatico**: Start con il sistema operativo
- [ ] 💾 **Profili**: Configurazioni salvabili e riutilizzabili
- [ ] ⌨️ **Hotkey Globali**: Controllo tramite scorciatoie da tastiera

### 📊 Funzionalità Avanzate
- [ ] 📈 **Statistiche**: Contatori e metriche dettagliate
- [ ] 🖱️ **Tipi di Click**: Destro, doppio, triplo click
- [ ] 🎭 **Sequenze**: Pattern di click personalizzati
- [ ] 📝 **File Logging**: Salvataggio log su disco
- [ ] 🌙 **Temi**: Modalità scura e chiara

### 🤝 Contributi
I contributi sono benvenuti! Sentiti libero di:
- 🐛 Segnalare bug
- 💡 Proporre nuove funzionalità
- 🔧 Inviare pull request
- 📖 Migliorare la documentazione

## 📄 Licenza

Questo progetto è rilasciato sotto **Licenza MIT**. Sei libero di:
- ✅ Usare il software per qualsiasi scopo
- ✅ Modificare il codice sorgente
- ✅ Distribuire copie del software
- ✅ Distribuire versioni modificate

## ⚠️ Disclaimer e Uso Responsabile

> **IMPORTANTE**: Usa questa applicazione in modo responsabile ed etico.

### 🚫 Limitazioni d'Uso
- ❌ Non utilizzare per violare **Termini di Servizio** di software/giochi
- ❌ Non utilizzare per attività fraudolente o dannose
- ❌ Non utilizzare per spam o automazioni massive

### 🛡️ Responsabilità
L'autore **Andrea Piani** non è responsabile per:
- Uso improprio del software
- Violazioni di ToS di terze parti
- Danni derivanti dall'utilizzo

### ✅ Usi Legittimi
- Test di interfacce utente
- Automazioni personali
- Scopi educativi
- Sviluppo e debugging

---

## 👨‍💻 Autore

**Andrea Piani**  
📧 Linktree e contatti: https://linktr.ee/andreapianidev
🐙 GitHub: [@andreapiani](https://github.com/andreapianidev)  

---

### ⭐ Ti è piaciuto il progetto?
Se questo progetto ti è stato utile, considera di:
- ⭐ Mettere una stella su GitHub
- 🍴 Fare un fork per i tuoi progetti
- 🐛 Segnalare bug o suggerimenti
- 📢 Condividere con altri sviluppatori

**Grazie per aver scelto Mouse Auto Clicker!** 🎉

## 🆕 Nuove Funzionalità di Sicurezza

La versione più recente include importanti miglioramenti alla sicurezza e alla stabilità dell'applicazione:

### 🛡️ Protezione Avanzata
- **Validazione Robusta**: Controlli completi su tutti gli input utente
- **Gestione Errori**: Sistema avanzato di rilevamento e recupero da errori
- **Limiti di Sicurezza**: Soglie automatiche per prevenire comportamenti anomali
- **Protezione Thread**: Terminazione sicura dei processi di click
- **Validazione Coordinate**: Controlli sui limiti dello schermo per evitare click fuori area

### 📁 Gestione Profili Migliorata
- **Operazioni Atomiche**: Salvataggio sicuro con file temporanei e backup
- **Validazione JSON**: Controlli strutturali sui file di configurazione
- **Limiti di Dimensione**: Protezione contro file di profilo eccessivamente grandi
- **Sanitizzazione Nomi**: Pulizia automatica dei nomi file per prevenire problemi

### 🔄 Sequenze di Click
- **Validazione Sequenze**: Controlli su lunghezza e validità delle sequenze
- **Controllo Errori**: Interruzione automatica dopo errori consecutivi
- **Validazione Click**: Controlli su tipo, coordinate e ritardi per ogni click

## 📸 Screenshot Nuova Versione

![Interfaccia Principale](https://www.andreapiani.com/autoclicker1.png)

*Interfaccia principale con nuove funzionalità di sicurezza*

![Gestione Profili](https://www.andreapiani.com/autoclicker2.png)

*Sistema migliorato di gestione profili*

![Sequenze di Click](https://www.andreapiani.com/autoclicker3.png)

*Editor avanzato di sequenze di click*

## 📞 Contatti per Modifiche

Hai bisogno di personalizzazioni o hai trovato un bug? Contattami:

- 📧 **Email**: Disponibile sul mio Linktree
- 🔗 **Linktree**: https://linktr.ee/andreapianidev
- 💬 **GitHub**: Apri una issue sul repository

Sono disponibile per implementare funzionalità personalizzate o risolvere problemi specifici secondo le tue esigenze.