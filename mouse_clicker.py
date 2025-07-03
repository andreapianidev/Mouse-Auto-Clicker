#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mouse Clicker - Applicazione per click automatici del mouse
Autore: Andrea Piani 12 4 2023
Descrizione: Simula click del mouse a intervalli casuali
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import random
import datetime
import pyautogui
import sys


class MouseClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Auto Clicker - Click Automatici")
        self.root.geometry("600x750")
        self.root.resizable(True, True)
        self.root.minsize(550, 650)
        
        # Variabili di controllo
        self.is_running = False
        self.click_thread = None
        self.click_count = 0
        
        # Configurazione pyautogui
        pyautogui.FAILSAFE = True  # Muovi mouse nell'angolo per fermare
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura l'interfaccia utente"""
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurazione griglia
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Titolo
        title_label = ttk.Label(main_frame, text="Mouse Auto Clicker", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Notebook per organizzare le impostazioni
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Tab 1: Impostazioni Base
        basic_frame = ttk.Frame(notebook, padding="10")
        notebook.add(basic_frame, text="Impostazioni Base")
        
        # Tab 2: Impostazioni Avanzate
        advanced_frame = ttk.Frame(notebook, padding="10")
        notebook.add(advanced_frame, text="Configurazione Avanzata")
        
        # === TAB IMPOSTAZIONI BASE ===
        # Frame per impostazioni intervallo
        interval_frame = ttk.LabelFrame(basic_frame, text="Intervallo Click (secondi)", 
                                       padding="10")
        interval_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), 
                           pady=(0, 10))
        interval_frame.columnconfigure(1, weight=1)
        interval_frame.columnconfigure(3, weight=1)
        
        # Campo intervallo minimo
        ttk.Label(interval_frame, text="Minimo:").grid(row=0, column=0, 
                                                      sticky=tk.W, padx=(0, 5))
        self.min_interval = tk.StringVar(value="1")
        min_spinbox = ttk.Spinbox(interval_frame, from_=0.1, to=3600, 
                                 increment=0.1, textvariable=self.min_interval,
                                 width=10)
        min_spinbox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20))
        
        # Campo intervallo massimo
        ttk.Label(interval_frame, text="Massimo:").grid(row=0, column=2, 
                                                       sticky=tk.W, padx=(0, 5))
        self.max_interval = tk.StringVar(value="5")
        max_spinbox = ttk.Spinbox(interval_frame, from_=0.1, to=3600, 
                                 increment=0.1, textvariable=self.max_interval,
                                 width=10)
        max_spinbox.grid(row=0, column=3, sticky=(tk.W, tk.E))
        
        # Frame per numero di click
        count_frame = ttk.LabelFrame(basic_frame, text="Numero di Click", padding="10")
        count_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        count_frame.columnconfigure(1, weight=1)
        
        # Opzione click infiniti
        self.infinite_clicks = tk.BooleanVar(value=True)
        infinite_check = ttk.Checkbutton(count_frame, text="Click infiniti", 
                                        variable=self.infinite_clicks,
                                        command=self.toggle_click_count)
        infinite_check.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        
        # Campo numero massimo click
        ttk.Label(count_frame, text="Numero massimo:").grid(row=0, column=1, sticky=tk.W, padx=(0, 5))
        self.max_clicks = tk.StringVar(value="100")
        self.max_clicks_spinbox = ttk.Spinbox(count_frame, from_=1, to=999999, 
                                            increment=1, textvariable=self.max_clicks,
                                            width=10, state='disabled')
        self.max_clicks_spinbox.grid(row=0, column=2, sticky=(tk.W, tk.E))
        
        # === TAB CONFIGURAZIONE AVANZATA ===
        # Frame tipo di click
        click_type_frame = ttk.LabelFrame(advanced_frame, text="Tipo di Click", padding="10")
        click_type_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.click_type = tk.StringVar(value="left")
        ttk.Radiobutton(click_type_frame, text="Click Sinistro", variable=self.click_type, 
                       value="left").grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Radiobutton(click_type_frame, text="Click Destro", variable=self.click_type, 
                       value="right").grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        ttk.Radiobutton(click_type_frame, text="Click Centrale", variable=self.click_type, 
                       value="middle").grid(row=0, column=2, sticky=tk.W)
        
        # Doppio click
        self.double_click = tk.BooleanVar(value=False)
        ttk.Checkbutton(click_type_frame, text="Doppio Click", 
                       variable=self.double_click).grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        # Frame posizione click
        position_frame = ttk.LabelFrame(advanced_frame, text="Posizione Click", padding="10")
        position_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        position_frame.columnconfigure(1, weight=1)
        position_frame.columnconfigure(3, weight=1)
        
        # Opzione posizione corrente vs fissa
        self.use_current_position = tk.BooleanVar(value=True)
        current_pos_check = ttk.Checkbutton(position_frame, text="Usa posizione corrente del mouse", 
                                          variable=self.use_current_position,
                                          command=self.toggle_position_mode)
        current_pos_check.grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 10))
        
        # Coordinate fisse
        ttk.Label(position_frame, text="X:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.fixed_x = tk.StringVar(value="100")
        self.x_spinbox = ttk.Spinbox(position_frame, from_=0, to=9999, 
                                   increment=1, textvariable=self.fixed_x,
                                   width=10, state='disabled')
        self.x_spinbox.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 20))
        
        ttk.Label(position_frame, text="Y:").grid(row=1, column=2, sticky=tk.W, padx=(0, 5))
        self.fixed_y = tk.StringVar(value="100")
        self.y_spinbox = ttk.Spinbox(position_frame, from_=0, to=9999, 
                                   increment=1, textvariable=self.fixed_y,
                                   width=10, state='disabled')
        self.y_spinbox.grid(row=1, column=3, sticky=(tk.W, tk.E))
        
        # Pulsante per catturare posizione corrente
        self.capture_button = ttk.Button(position_frame, text="📍 Cattura Posizione Corrente", 
                                        command=self.capture_current_position,
                                        state='disabled')
        self.capture_button.grid(row=2, column=0, columnspan=4, pady=(10, 0))
        
        # Frame opzioni avanzate
        options_frame = ttk.LabelFrame(advanced_frame, text="Opzioni Avanzate", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Ritardo iniziale
        ttk.Label(options_frame, text="Ritardo iniziale (secondi):").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.initial_delay = tk.StringVar(value="3")
        ttk.Spinbox(options_frame, from_=0, to=60, increment=1, 
                   textvariable=self.initial_delay, width=10).grid(row=0, column=1, sticky=tk.W)
        
        # Suono di notifica
        self.play_sound = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Suono di notifica", 
                       variable=self.play_sound).grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        # Minimizza durante l'esecuzione
        self.minimize_on_start = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Minimizza finestra durante l'esecuzione", 
                       variable=self.minimize_on_start).grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        
        # Frame per pulsanti di controllo
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        # Pulsante Avvia
        self.start_button = ttk.Button(control_frame, text="▶ Avvia", 
                                      command=self.start_clicking,
                                      style='Accent.TButton')
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        # Pulsante Ferma
        self.stop_button = ttk.Button(control_frame, text="⏹ Ferma", 
                                     command=self.stop_clicking,
                                     state='disabled')
        self.stop_button.grid(row=0, column=1)
        
        # Stato applicazione e contatori
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        self.status_var = tk.StringVar(value="Pronto")
        status_label = ttk.Label(status_frame, textvariable=self.status_var,
                                font=('Arial', 10, 'bold'))
        status_label.grid(row=0, column=0, padx=(0, 20))
        
        # Contatore click
        self.click_counter_var = tk.StringVar(value="Click eseguiti: 0")
        counter_label = ttk.Label(status_frame, textvariable=self.click_counter_var,
                                 font=('Arial', 9))
        counter_label.grid(row=0, column=1)
        
        # Pulsante reset contatore
        reset_button = ttk.Button(status_frame, text="Reset", 
                                 command=self.reset_counter, width=8)
        reset_button.grid(row=0, column=2, padx=(10, 0))
        
        # Frame per log
        log_frame = ttk.LabelFrame(main_frame, text="Log Click", padding="5")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S),
                      pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Area di testo per log
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, 
                                                 state='disabled',
                                                 wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Pulsante per pulire log
        clear_log_button = ttk.Button(log_frame, text="Pulisci Log", 
                                     command=self.clear_log)
        clear_log_button.grid(row=1, column=0, pady=(5, 0))
        
        # Info e istruzioni
        info_frame = ttk.LabelFrame(main_frame, text="Informazioni", padding="5")
        info_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        info_text = (
            "• Configura tutti i parametri nelle schede sopra\n"
            "• Muovi il mouse nell'angolo superiore sinistro per fermare d'emergenza\n"
            "• Usa il ritardo iniziale per posizionare il mouse prima dell'avvio"
        )
        ttk.Label(info_frame, text=info_text, font=('Arial', 9)).grid(row=0, column=0)
        
        # Gestione chiusura finestra
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Log iniziale
        self.log_message("Applicazione avviata. Pronta per l'uso.")
    
    def toggle_click_count(self):
        """Abilita/disabilita il campo numero massimo click"""
        if self.infinite_clicks.get():
            self.max_clicks_spinbox.config(state='disabled')
        else:
            self.max_clicks_spinbox.config(state='normal')
    
    def toggle_position_mode(self):
        """Abilita/disabilita i campi per coordinate fisse"""
        if self.use_current_position.get():
            self.x_spinbox.config(state='disabled')
            self.y_spinbox.config(state='disabled')
            self.capture_button.config(state='disabled')
        else:
            self.x_spinbox.config(state='normal')
            self.y_spinbox.config(state='normal')
            self.capture_button.config(state='normal')
    
    def capture_current_position(self):
        """Cattura la posizione corrente del mouse"""
        try:
            current_pos = pyautogui.position()
            self.fixed_x.set(str(current_pos.x))
            self.fixed_y.set(str(current_pos.y))
            self.log_message(f"Posizione catturata: ({current_pos.x}, {current_pos.y})")
        except Exception as e:
            self.log_message(f"Errore nel catturare la posizione: {str(e)}")
    
    def reset_counter(self):
        """Resetta il contatore dei click"""
        self.click_count = 0
        self.click_counter_var.set("Click eseguiti: 0")
        self.log_message("Contatore click resettato")
    
    def play_notification_sound(self):
        """Riproduce un suono di notifica (se abilitato)"""
        if self.play_sound.get():
            try:
                # Usa il suono di sistema (funziona su Windows/Mac/Linux)
                import winsound
                winsound.Beep(1000, 200)  # Frequenza 1000Hz per 200ms
            except ImportError:
                try:
                    # Alternativa per macOS/Linux
                    import os
                    os.system('afplay /System/Library/Sounds/Glass.aiff')
                except:
                    # Fallback: stampa un messaggio
                    print("\a")  # Beep del terminale
        
    def validate_intervals(self):
        """Valida gli intervalli inseriti dall'utente"""
        try:
            min_val = float(self.min_interval.get())
            max_val = float(self.max_interval.get())
            
            if min_val <= 0 or max_val <= 0:
                raise ValueError("Gli intervalli devono essere maggiori di 0")
                
            if min_val > max_val:
                raise ValueError("L'intervallo minimo deve essere minore del massimo")
                
            return min_val, max_val
            
        except ValueError as e:
            if "could not convert" in str(e):
                messagebox.showerror("Errore", "Inserisci valori numerici validi")
            else:
                messagebox.showerror("Errore", str(e))
            return None, None
    
    def validate_configuration(self):
        """Valida tutta la configurazione prima di iniziare"""
        # Valida intervalli
        min_val, max_val = self.validate_intervals()
        if min_val is None:
            return False
        
        # Valida numero massimo click se non infiniti
        if not self.infinite_clicks.get():
            try:
                max_clicks = int(self.max_clicks.get())
                if max_clicks <= 0:
                    raise ValueError("Il numero massimo di click deve essere maggiore di 0")
            except ValueError:
                messagebox.showerror("Errore", "Inserisci un numero valido per il massimo di click")
                return False
        
        # Valida coordinate fisse se selezionate
        if not self.use_current_position.get():
            try:
                x = int(self.fixed_x.get())
                y = int(self.fixed_y.get())
                if x < 0 or y < 0:
                    raise ValueError("Le coordinate devono essere positive")
            except ValueError:
                messagebox.showerror("Errore", "Inserisci coordinate valide")
                return False
        
        # Valida ritardo iniziale
        try:
            delay = float(self.initial_delay.get())
            if delay < 0:
                raise ValueError("Il ritardo iniziale deve essere positivo")
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un ritardo iniziale valido")
            return False
        
        return True
    
    def start_clicking(self):
        """Avvia il ciclo di click automatici"""
        # Valida tutta la configurazione
        if not self.validate_configuration():
            return
        
        # Resetta il contatore se necessario
        if not self.infinite_clicks.get():
            self.click_count = 0
            self.click_counter_var.set("Click eseguiti: 0")
        
        self.is_running = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status_var.set("In esecuzione...")
        
        # Minimizza finestra se richiesto
        if self.minimize_on_start.get():
            self.root.iconify()
        
        # Avvia thread per i click
        self.click_thread = threading.Thread(target=self.click_loop_advanced,
                                            daemon=True)
        self.click_thread.start()
        
        min_val = float(self.min_interval.get())
        max_val = float(self.max_interval.get())
        click_type = self.click_type.get()
        max_clicks = "∞" if self.infinite_clicks.get() else self.max_clicks.get()
        
        self.log_message(f"Click automatici avviati:")
        self.log_message(f"  • Intervallo: {min_val}-{max_val}s")
        self.log_message(f"  • Tipo: {click_type.upper()}")
        self.log_message(f"  • Numero massimo: {max_clicks}")
        self.log_message(f"  • Doppio click: {'Sì' if self.double_click.get() else 'No'}")
        
        # Suono di avvio
        self.play_notification_sound()
    
    def stop_clicking(self):
        """Ferma il ciclo di click automatici"""
        self.is_running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_var.set("Fermato")
        
        # Ripristina finestra se era minimizzata
        if self.root.state() == 'iconic':
            self.root.deiconify()
        
        self.log_message("Click automatici fermati")
        
        # Suono di stop
        self.play_notification_sound()
    
    def click_loop_advanced(self):
        """Loop principale avanzato per i click automatici"""
        try:
            # Ottieni configurazione
            min_interval = float(self.min_interval.get())
            max_interval = float(self.max_interval.get())
            initial_delay = float(self.initial_delay.get())
            max_clicks = None if self.infinite_clicks.get() else int(self.max_clicks.get())
            
            # Ritardo iniziale
            if initial_delay > 0:
                self.log_message(f"Ritardo iniziale di {initial_delay} secondi...")
                start_delay = time.time()
                while time.time() - start_delay < initial_delay and self.is_running:
                    remaining = initial_delay - (time.time() - start_delay)
                    self.root.after(0, lambda: self.status_var.set(f"Avvio tra {remaining:.1f}s..."))
                    time.sleep(0.1)
                
                if not self.is_running:
                    return
                
                self.root.after(0, lambda: self.status_var.set("In esecuzione..."))
            
            while self.is_running:
                # Controlla se abbiamo raggiunto il numero massimo
                if max_clicks is not None and self.click_count >= max_clicks:
                    self.log_message(f"Raggiunto numero massimo di click ({max_clicks})")
                    self.root.after(0, self.stop_clicking)
                    break
                
                # Genera intervallo casuale
                wait_time = random.uniform(min_interval, max_interval)
                
                # Attendi (controllando se dobbiamo fermarci)
                start_wait = time.time()
                while time.time() - start_wait < wait_time and self.is_running:
                    time.sleep(0.1)
                
                if not self.is_running:
                    break
                
                # Determina posizione del click
                if self.use_current_position.get():
                    click_pos = pyautogui.position()
                else:
                    click_pos = (int(self.fixed_x.get()), int(self.fixed_y.get()))
                
                # Esegui click
                try:
                    if self.double_click.get():
                        pyautogui.doubleClick(x=click_pos[0], y=click_pos[1], 
                                            button=self.click_type.get())
                        click_description = "Doppio click"
                    else:
                        pyautogui.click(x=click_pos[0], y=click_pos[1], 
                                      button=self.click_type.get())
                        click_description = "Click"
                    
                    # Aggiorna contatore
                    self.click_count += 1
                    self.root.after(0, lambda: self.click_counter_var.set(f"Click eseguiti: {self.click_count}"))
                    
                    # Log del click
                    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                    button_name = self.click_type.get().upper()
                    remaining_text = ""
                    if max_clicks is not None:
                        remaining = max_clicks - self.click_count
                        remaining_text = f" (rimangono: {remaining})"
                    
                    log_msg = (f"[{timestamp}] {click_description} {button_name} in ({click_pos[0]}, {click_pos[1]}) "
                              f"- Attesa: {wait_time:.1f}s{remaining_text}")
                    self.log_message(log_msg)
                    
                except pyautogui.FailSafeException:
                    self.log_message("[EMERGENZA] Click fermati - mouse nell'angolo")
                    self.root.after(0, self.stop_clicking)
                    break
                except Exception as e:
                    self.log_message(f"[ERRORE] Errore durante il click: {str(e)}")
                    
        except Exception as e:
            self.log_message(f"[ERRORE] Errore nel loop di click: {str(e)}")
            self.root.after(0, self.stop_clicking)
    
    def log_message(self, message):
        """Aggiunge un messaggio al log"""
        def update_log():
            self.log_text.config(state='normal')
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.log_text.see(tk.END)
            self.log_text.config(state='disabled')
        
        # Esegui aggiornamento nel thread principale
        if threading.current_thread() == threading.main_thread():
            update_log()
        else:
            self.root.after(0, update_log)
    
    def clear_log(self):
        """Pulisce il log"""
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        self.log_message("Log pulito")
    
    def on_closing(self):
        """Gestisce la chiusura dell'applicazione"""
        if self.is_running:
            if messagebox.askokcancel("Chiusura", 
                                    "I click sono ancora attivi. Vuoi fermarli e chiudere?"):
                self.stop_clicking()
                time.sleep(0.2)  # Piccola pausa per fermare il thread
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Funzione principale"""
    try:
        # Verifica dipendenze
        import pyautogui
    except ImportError:
        print("Errore: pyautogui non installato. Installa con: pip install pyautogui")
        sys.exit(1)
    
    # Crea e avvia applicazione
    root = tk.Tk()
    app = MouseClickerApp(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nApplicazione chiusa dall'utente")
    except Exception as e:
        print(f"Errore nell'applicazione: {e}")
        messagebox.showerror("Errore Critico", f"Errore nell'applicazione: {e}")


if __name__ == "__main__":
    main()


# TODO: Miglioramenti futuri
# - Implementare minimizzazione nella system tray
# - Aggiungere opzione per click in coordinate fisse
# - Implementare avvio automatico all'avvio del sistema
# - Aggiungere profili salvabili per diverse configurazioni
# - Implementare hotkey globali per start/stop
# - Aggiungere statistiche sui click (totali, velocità media, ecc.)
# - Implementare diversi tipi di click (sinistro, destro, doppio)
# - Aggiungere opzione per sequenze di click personalizzate
# - Implementare logging su file
# - Aggiungere tema scuro/chiaro