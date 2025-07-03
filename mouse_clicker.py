#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mouse Auto Clicker - Applicazione per click automatici del mouse
Autore: Andrea Piani 12 4 2023
Descrizione: Simula click del mouse a intervalli casuali 
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog, simpledialog
import threading
import time
import random
import datetime
import pyautogui
import sys
import json
import os
from typing import List, Dict, Tuple, Optional


# === CLASSE DIALOG PER CLICK ===

class ClickDialog:
    """Dialog per aggiungere/modificare click nelle sequenze"""
    
    def __init__(self, parent, title, click_data=None):
        self.result = None
        
        # Crea finestra dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x350")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centra la finestra
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (350 // 2)
        self.dialog.geometry(f"400x350+{x}+{y}")
        
        # Variabili
        self.x_var = tk.StringVar(value=str(click_data.get('x', 100)) if click_data else "100")
        self.y_var = tk.StringVar(value=str(click_data.get('y', 100)) if click_data else "100")
        self.button_var = tk.StringVar(value=click_data.get('button', 'left') if click_data else 'left')
        self.double_var = tk.BooleanVar(value=click_data.get('double', False) if click_data else False)
        self.delay_var = tk.StringVar(value=str(click_data.get('delay', 1.0)) if click_data else "1.0")
        
        self.setup_ui()
        
        # Aspetta che la finestra sia chiusa
        self.dialog.wait_window()
    
    def setup_ui(self):
        """Configura l'interfaccia del dialog"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titolo
        title_label = ttk.Label(main_frame, text="Configurazione Click", font=('Arial', 12, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Frame per coordinate
        coord_frame = ttk.LabelFrame(main_frame, text="Coordinate", padding="10")
        coord_frame.pack(fill=tk.X, pady=(0, 10))
        
        # X coordinate
        x_frame = ttk.Frame(coord_frame)
        x_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(x_frame, text="X:").pack(side=tk.LEFT)
        ttk.Entry(x_frame, textvariable=self.x_var, width=10).pack(side=tk.LEFT, padx=(5, 0))
        
        # Y coordinate
        y_frame = ttk.Frame(coord_frame)
        y_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(y_frame, text="Y:").pack(side=tk.LEFT)
        ttk.Entry(y_frame, textvariable=self.y_var, width=10).pack(side=tk.LEFT, padx=(5, 0))
        
        # Pulsante per ottenere posizione corrente
        ttk.Button(coord_frame, text="📍 Usa Posizione Corrente", 
                  command=self.get_current_position).pack(pady=(5, 0))
        
        # Frame per tipo di click
        click_frame = ttk.LabelFrame(main_frame, text="Tipo di Click", padding="10")
        click_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Pulsanti radio per tipo
        button_frame = ttk.Frame(click_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Radiobutton(button_frame, text="Sinistro", variable=self.button_var, 
                       value="left").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(button_frame, text="Destro", variable=self.button_var, 
                       value="right").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(button_frame, text="Centrale", variable=self.button_var, 
                       value="middle").pack(side=tk.LEFT)
        
        # Checkbox per doppio click
        ttk.Checkbutton(click_frame, text="Doppio Click", 
                       variable=self.double_var).pack(pady=(10, 0))
        
        # Frame per delay
        delay_frame = ttk.LabelFrame(main_frame, text="Pausa dopo il Click (secondi)", padding="10")
        delay_frame.pack(fill=tk.X, pady=(0, 20))
        
        delay_entry_frame = ttk.Frame(delay_frame)
        delay_entry_frame.pack(fill=tk.X)
        ttk.Entry(delay_entry_frame, textvariable=self.delay_var, width=10).pack(side=tk.LEFT)
        ttk.Label(delay_entry_frame, text="secondi").pack(side=tk.LEFT, padx=(5, 0))
        
        # Pulsanti
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="✅ OK", command=self.ok_clicked).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="❌ Annulla", command=self.cancel_clicked).pack(side=tk.RIGHT)
    
    def get_current_position(self):
        """Ottiene la posizione corrente del mouse"""
        try:
            # Nascondi temporaneamente la finestra
            self.dialog.withdraw()
            
            # Aspetta un momento per permettere all'utente di posizionare il mouse
            self.dialog.after(1000, self._get_position)
            
        except Exception as e:
            tk.messagebox.showerror("Errore", f"Errore nell'ottenere la posizione: {str(e)}")
            self.dialog.deiconify()
    
    def _get_position(self):
        """Ottiene effettivamente la posizione del mouse"""
        try:
            import pyautogui
            x, y = pyautogui.position()
            self.x_var.set(str(x))
            self.y_var.set(str(y))
            
            # Mostra di nuovo la finestra
            self.dialog.deiconify()
            
        except Exception as e:
            tk.messagebox.showerror("Errore", f"Errore nell'ottenere la posizione: {str(e)}")
            self.dialog.deiconify()
    
    def ok_clicked(self):
        """Gestisce il click su OK con validazione robusta"""
        try:
            # Valida le coordinate
            x_str = self.x_var.get().strip()
            y_str = self.y_var.get().strip()
            delay_str = self.delay_var.get().strip()
            
            if not x_str or not y_str or not delay_str:
                raise ValueError("Tutti i campi devono essere compilati")
            
            x = int(x_str)
            y = int(y_str)
            delay = float(delay_str)
            
            # Validazione coordinate
            if x < 0 or y < 0:
                raise ValueError("Le coordinate devono essere positive")
            
            if x > 32767 or y > 32767:  # Limite ragionevole per le coordinate
                raise ValueError("Le coordinate sono troppo grandi (max 32767)")
            
            # Validazione delay
            if delay < 0:
                raise ValueError("Il delay non può essere negativo")
            
            if delay > 3600:  # Più di 1 ora
                if not tk.messagebox.askyesno("Attenzione", 
                                             f"Hai impostato un delay molto lungo ({delay}s). Continuare?"):
                    return
            
            # Verifica che le coordinate siano entro i limiti dello schermo
            try:
                import pyautogui
                screen_width, screen_height = pyautogui.size()
                if x >= screen_width or y >= screen_height:
                    if not tk.messagebox.askyesno("Attenzione", 
                                                 f"Le coordinate ({x}, {y}) sono fuori dallo schermo ({screen_width}x{screen_height}). Continuare?"):
                        return
            except Exception:
                pass  # Se non riusciamo a ottenere le dimensioni dello schermo, continuiamo
            
            # Crea il risultato
            self.result = {
                'x': x,
                'y': y,
                'button': self.button_var.get(),
                'double': self.double_var.get(),
                'delay': delay
            }
            
            self.dialog.destroy()
            
        except ValueError as e:
            tk.messagebox.showerror("Errore", f"Dati non validi: {str(e)}")
        except Exception as e:
            tk.messagebox.showerror("Errore", f"Errore imprevisto: {str(e)}")
    
    def cancel_clicked(self):
        """Gestisce il click su Annulla"""
        self.result = None
        self.dialog.destroy()


# === CLASSE PRINCIPALE ===

class MouseClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Auto Clicker - Click Automatici")
        self.root.geometry("900x1000")
        self.root.resizable(True, True)
        self.root.minsize(900, 1000)
        
        # Variabili di controllo
        self.is_running = False
        self.click_thread = None
        self.click_count = 0
        
        # Variabili per sequenze e macro
        self.is_recording = False
        self.recorded_sequence = []
        self.current_sequence = []
        self.sequence_mode = False
        
        # Profili
        self.profiles_dir = "profiles"
        self.current_profile = None
        
        # Crea directory profili se non esiste
        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir)
        
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
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)  # Il notebook si espande
        main_frame.rowconfigure(4, weight=1)  # Il log si espande
        
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
        basic_frame.columnconfigure(0, weight=1)
        basic_frame.columnconfigure(1, weight=1)
        
        # Tab 2: Impostazioni Avanzate
        advanced_frame = ttk.Frame(notebook, padding="10")
        notebook.add(advanced_frame, text="Configurazione Avanzata")
        advanced_frame.columnconfigure(0, weight=1)
        advanced_frame.columnconfigure(1, weight=1)
        
        # Tab 3: Sequenze e Macro
        sequence_frame = ttk.Frame(notebook, padding="10")
        notebook.add(sequence_frame, text="Sequenze e Macro")
        
        # Tab 4: Profili
        profiles_frame = ttk.Frame(notebook, padding="10")
        notebook.add(profiles_frame, text="Profili")
        
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
        
        # === TAB SEQUENZE E MACRO ===
        self.setup_sequence_tab(sequence_frame)
        
        # === TAB PROFILI ===
        self.setup_profiles_tab(profiles_frame)
        
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
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, 
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
    
    def setup_sequence_tab(self, parent):
        """Configura il tab per sequenze e macro"""
        # Configurazione griglia per il tab
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(2, weight=1)  # Frame sequenza corrente si espande
        
        # Frame modalità sequenza
        mode_frame = ttk.LabelFrame(parent, text="Modalità di Esecuzione", padding="10")
        mode_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.execution_mode = tk.StringVar(value="single")
        ttk.Radiobutton(mode_frame, text="Click Singoli", variable=self.execution_mode, 
                       value="single", command=self.toggle_execution_mode).grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Radiobutton(mode_frame, text="Sequenza Personalizzata", variable=self.execution_mode, 
                       value="sequence", command=self.toggle_execution_mode).grid(row=0, column=1, sticky=tk.W)
        
        # Frame registrazione macro
        record_frame = ttk.LabelFrame(parent, text="Registrazione Macro", padding="10")
        record_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.record_button = ttk.Button(record_frame, text="🔴 Inizia Registrazione", 
                                       command=self.toggle_recording)
        self.record_button.grid(row=0, column=0, padx=(0, 10))
        
        self.clear_sequence_button = ttk.Button(record_frame, text="🗑️ Cancella Sequenza", 
                                              command=self.clear_sequence)
        self.clear_sequence_button.grid(row=0, column=1, padx=(0, 10))
        
        # Stato registrazione
        self.recording_status = tk.StringVar(value="Pronto per registrare")
        ttk.Label(record_frame, textvariable=self.recording_status, 
                 font=('Arial', 9, 'italic')).grid(row=1, column=0, columnspan=2, pady=(5, 0))
        
        # Frame sequenza corrente
        current_seq_frame = ttk.LabelFrame(parent, text="Sequenza Corrente", padding="10")
        current_seq_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        current_seq_frame.columnconfigure(0, weight=1)
        current_seq_frame.rowconfigure(0, weight=1)
        
        # Lista sequenza
        self.sequence_listbox = tk.Listbox(current_seq_frame, height=8)
        self.sequence_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Scrollbar per lista
        seq_scrollbar = ttk.Scrollbar(current_seq_frame, orient="vertical", command=self.sequence_listbox.yview)
        seq_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.sequence_listbox.configure(yscrollcommand=seq_scrollbar.set)
        
        # Pulsanti gestione sequenza
        seq_buttons_frame = ttk.Frame(current_seq_frame)
        seq_buttons_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(seq_buttons_frame, text="➕ Aggiungi Click Manuale", 
                  command=self.add_manual_click).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(seq_buttons_frame, text="✏️ Modifica Selezionato", 
                  command=self.edit_selected_click).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(seq_buttons_frame, text="🗑️ Rimuovi Selezionato", 
                  command=self.remove_selected_click).grid(row=0, column=2)
        
        # Frame opzioni sequenza
        seq_options_frame = ttk.LabelFrame(parent, text="Opzioni Sequenza", padding="10")
        seq_options_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Ripetizioni sequenza
        ttk.Label(seq_options_frame, text="Ripetizioni sequenza:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.sequence_repeats = tk.StringVar(value="1")
        ttk.Spinbox(seq_options_frame, from_=1, to=9999, increment=1, 
                   textvariable=self.sequence_repeats, width=10).grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Pausa tra ripetizioni
        ttk.Label(seq_options_frame, text="Pausa tra ripetizioni (s):").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.sequence_pause = tk.StringVar(value="1.0")
        ttk.Spinbox(seq_options_frame, from_=0.1, to=60, increment=0.1, 
                   textvariable=self.sequence_pause, width=10).grid(row=0, column=3, sticky=tk.W)
        
        # Sequenza infinita
        self.infinite_sequence = tk.BooleanVar(value=False)
        ttk.Checkbutton(seq_options_frame, text="Ripeti sequenza infinitamente", 
                       variable=self.infinite_sequence, 
                       command=self.toggle_infinite_sequence).grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=(10, 0))
    
    def setup_profiles_tab(self, parent):
        """Configura il tab per i profili"""
        # Configurazione griglia per il tab
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(2, weight=1)  # Frame profili disponibili si espande
        
        # Frame profilo corrente
        current_profile_frame = ttk.LabelFrame(parent, text="Profilo Corrente", padding="10")
        current_profile_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.current_profile_var = tk.StringVar(value="Nessun profilo caricato")
        ttk.Label(current_profile_frame, textvariable=self.current_profile_var, 
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
        
        # Frame gestione profili
        profile_mgmt_frame = ttk.LabelFrame(parent, text="Gestione Profili", padding="10")
        profile_mgmt_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Pulsanti gestione
        ttk.Button(profile_mgmt_frame, text="💾 Salva Profilo", 
                  command=self.save_profile).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(profile_mgmt_frame, text="📂 Carica Profilo", 
                  command=self.load_profile).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(profile_mgmt_frame, text="📤 Esporta Profilo", 
                  command=self.export_profile).grid(row=0, column=2, padx=(0, 10))
        ttk.Button(profile_mgmt_frame, text="📥 Importa Profilo", 
                  command=self.import_profile).grid(row=0, column=3)
        
        # Frame profili disponibili
        available_profiles_frame = ttk.LabelFrame(parent, text="Profili Disponibili", padding="10")
        available_profiles_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        available_profiles_frame.columnconfigure(0, weight=1)
        available_profiles_frame.rowconfigure(0, weight=1)
        
        # Lista profili
        self.profiles_listbox = tk.Listbox(available_profiles_frame, height=8)
        self.profiles_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        self.profiles_listbox.bind('<Double-1>', self.load_selected_profile)
        
        # Scrollbar per lista profili
        profiles_scrollbar = ttk.Scrollbar(available_profiles_frame, orient="vertical", 
                                         command=self.profiles_listbox.yview)
        profiles_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.profiles_listbox.configure(yscrollcommand=profiles_scrollbar.set)
        
        # Pulsanti gestione profili
        profile_buttons_frame = ttk.Frame(available_profiles_frame)
        profile_buttons_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(profile_buttons_frame, text="🔄 Aggiorna Lista", 
                  command=self.refresh_profiles_list).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(profile_buttons_frame, text="🗑️ Elimina Profilo", 
                  command=self.delete_selected_profile).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(profile_buttons_frame, text="📋 Duplica Profilo", 
                  command=self.duplicate_selected_profile).grid(row=0, column=2)
        
        # Frame profili predefiniti
        preset_profiles_frame = ttk.LabelFrame(parent, text="Profili Predefiniti", padding="10")
        preset_profiles_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(preset_profiles_frame, text="🎮 Gaming (Click Rapidi)", 
                  command=lambda: self.load_preset_profile("gaming")).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(preset_profiles_frame, text="🏢 Ufficio (Click Lenti)", 
                  command=lambda: self.load_preset_profile("office")).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(preset_profiles_frame, text="🧪 Test (Click Medi)", 
                  command=lambda: self.load_preset_profile("test")).grid(row=0, column=2)
        
        # Carica lista profili iniziale
        self.refresh_profiles_list()
    
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
                import platform
                system = platform.system()
                
                if system == "Windows":
                    import winsound
                    winsound.Beep(1000, 200)
                elif system == "Darwin":  # macOS
                    import subprocess
                    subprocess.run(['afplay', '/System/Library/Sounds/Glass.aiff'], 
                                 check=False, capture_output=True)
                elif system == "Linux":
                    import subprocess
                    subprocess.run(['paplay', '/usr/share/sounds/alsa/Front_Left.wav'], 
                                 check=False, capture_output=True)
                else:
                    print("\a")  # Fallback universale
            except Exception as e:
                print("\a")  # Fallback in caso di errore
        
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
            initial_delay = float(self.initial_delay.get())
            
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
            
            # Esegui modalità appropriata
            if self.sequence_mode and self.current_sequence:
                self.execute_sequence()
            else:
                self.execute_single_clicks()
                    
        except Exception as e:
            self.log_message(f"[ERRORE] Errore nel loop di click: {str(e)}")
            self.root.after(0, self.stop_clicking)
    
    def execute_single_clicks(self):
        """Esegue click singoli tradizionali con controlli di sicurezza"""
        try:
            min_interval = float(self.min_interval.get())
            max_interval = float(self.max_interval.get())
            max_clicks = None if self.infinite_clicks.get() else int(self.max_clicks.get())
            
            # Validazione parametri
            if min_interval < 0 or max_interval < 0 or min_interval > max_interval:
                self.log_message("[ERRORE] Intervalli non validi")
                self.root.after(0, self.stop_clicking)
                return
            
            if max_clicks is not None and max_clicks <= 0:
                self.log_message("[ERRORE] Numero massimo click non valido")
                self.root.after(0, self.stop_clicking)
                return
            
            consecutive_errors = 0
            max_consecutive_errors = 5
            
            while self.is_running:
                # Controlla se abbiamo raggiunto il numero massimo
                if max_clicks is not None and self.click_count >= max_clicks:
                    self.log_message(f"Raggiunto numero massimo di click ({max_clicks})")
                    self.root.after(0, self.stop_clicking)
                    break
                
                # Controlla errori consecutivi
                if consecutive_errors >= max_consecutive_errors:
                    self.log_message(f"[ERRORE] Troppi errori consecutivi ({consecutive_errors}), fermando")
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
                
                # Determina posizione del click con validazione
                try:
                    if self.use_current_position.get():
                        click_pos = pyautogui.position()
                    else:
                        fixed_x = int(self.fixed_x.get())
                        fixed_y = int(self.fixed_y.get())
                        
                        # Validazione coordinate fisse
                        if fixed_x < 0 or fixed_y < 0 or fixed_x > 32767 or fixed_y > 32767:
                            self.log_message(f"[ERRORE] Coordinate fisse non valide: ({fixed_x}, {fixed_y})")
                            consecutive_errors += 1
                            continue
                        
                        click_pos = (fixed_x, fixed_y)
                    
                    # Verifica che le coordinate siano valide
                    if click_pos[0] < 0 or click_pos[1] < 0:
                        self.log_message(f"[ERRORE] Coordinate negative: {click_pos}")
                        consecutive_errors += 1
                        continue
                        
                except (ValueError, TypeError) as e:
                    self.log_message(f"[ERRORE] Errore nelle coordinate: {str(e)}")
                    consecutive_errors += 1
                    continue
                
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
                    
                    # Reset contatore errori se il click è riuscito
                    consecutive_errors = 0
                    
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
                    consecutive_errors += 1
                    self.log_message(f"[ERRORE] Errore durante il click: {str(e)}")
                    
                    # Pausa breve dopo un errore
                    if self.is_running:
                        time.sleep(0.5)
                        
        except Exception as e:
            self.log_message(f"[ERRORE CRITICO] Errore nel metodo execute_single_clicks: {str(e)}")
            self.root.after(0, self.stop_clicking)
    
    def execute_sequence(self):
        """Esegue una sequenza di click personalizzata con controlli di sicurezza"""
        try:
            if not self.current_sequence:
                self.log_message("Nessuna sequenza definita")
                return
            
            # Validazione parametri
            try:
                max_repeats = int(self.sequence_repeats.get()) if not self.infinite_sequence.get() else float('inf')
                sequence_pause = float(self.sequence_pause.get())
                
                if max_repeats <= 0 and not self.infinite_sequence.get():
                    self.log_message("[ERRORE] Numero di ripetizioni non valido")
                    self.root.after(0, self.stop_clicking)
                    return
                    
                if sequence_pause < 0:
                    self.log_message("[ERRORE] Pausa sequenza non valida")
                    self.root.after(0, self.stop_clicking)
                    return
            except (ValueError, TypeError) as e:
                self.log_message(f"[ERRORE] Parametri sequenza non validi: {str(e)}")
                self.root.after(0, self.stop_clicking)
                return
            
            sequence_count = 0
            consecutive_errors = 0
            max_consecutive_errors = 5
            
            self.log_message(f"Iniziando sequenza con {len(self.current_sequence)} click")
            
            while self.is_running and sequence_count < max_repeats:
                # Controlla errori consecutivi
                if consecutive_errors >= max_consecutive_errors:
                    self.log_message(f"[ERRORE] Troppi errori consecutivi ({consecutive_errors}), fermando")
                    self.root.after(0, self.stop_clicking)
                    break
                    
                sequence_count += 1
                self.log_message(f"Esecuzione sequenza #{sequence_count}")
                
                for i, click_data in enumerate(self.current_sequence):
                    if not self.is_running:
                        break
                    
                    try:
                        # Estrai e valida dati del click
                        if not isinstance(click_data, dict):
                            self.log_message(f"[ERRORE] Dati click {i+1} non validi")
                            consecutive_errors += 1
                            continue
                            
                        # Estrai dati con validazione
                        try:
                            x = int(click_data.get('x', 0))
                            y = int(click_data.get('y', 0))
                            button = click_data.get('button', 'left')
                            is_double = bool(click_data.get('double', False))
                            delay = float(click_data.get('delay', 1.0))
                            
                            # Validazione coordinate
                            if x < 0 or y < 0 or x > 32767 or y > 32767:
                                self.log_message(f"[ERRORE] Coordinate non valide nel click {i+1}: ({x}, {y})")
                                consecutive_errors += 1
                                continue
                                
                            # Validazione delay
                            if delay < 0:
                                delay = 0.1  # Correggi automaticamente
                                self.log_message(f"[AVVISO] Delay negativo corretto nel click {i+1}")
                                
                            # Validazione button
                            if button not in ['left', 'middle', 'right']:
                                button = 'left'  # Correggi automaticamente
                                self.log_message(f"[AVVISO] Tipo click non valido corretto nel click {i+1}")
                                
                        except (ValueError, TypeError) as e:
                            self.log_message(f"[ERRORE] Dati click {i+1} non validi: {str(e)}")
                            consecutive_errors += 1
                            continue
                        
                        # Esegui il click
                        if is_double:
                            pyautogui.doubleClick(x, y, button=button)
                            click_description = "Doppio click"
                        else:
                            pyautogui.click(x, y, button=button)
                            click_description = "Click"
                        
                        # Reset contatore errori se il click è riuscito
                        consecutive_errors = 0
                        
                        # Aggiorna contatore
                        self.click_count += 1
                        self.root.after(0, lambda count=sequence_count: 
                                      self.click_counter_var.set(f"Click eseguiti: {self.click_count} (Seq: {count})"))
                        
                        # Log del click
                        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                        log_msg = f"[{timestamp}] Seq {sequence_count}.{i+1}: {click_description} {button.upper()} in ({x}, {y})"
                        self.log_message(log_msg)
                        
                        # Pausa tra click nella sequenza
                        if self.is_running and i < len(self.current_sequence) - 1:
                            start_wait = time.time()
                            while time.time() - start_wait < delay and self.is_running:
                                time.sleep(0.1)
                        
                    except pyautogui.FailSafeException:
                        self.log_message("[EMERGENZA] Click fermati - mouse nell'angolo")
                        self.root.after(0, self.stop_clicking)
                        return
                    except Exception as e:
                        consecutive_errors += 1
                        self.log_message(f"[ERRORE] Errore durante il click {i+1} della sequenza: {str(e)}")
                        
                        # Pausa breve dopo un errore
                        if self.is_running:
                            time.sleep(0.5)
                            continue
                
                # Pausa tra ripetizioni della sequenza
                if self.is_running and sequence_count < max_repeats:
                    self.log_message(f"Pausa di {sequence_pause}s prima della prossima sequenza")
                    start_wait = time.time()
                    while time.time() - start_wait < sequence_pause and self.is_running:
                        time.sleep(0.1)
            
            self.log_message(f"Sequenza completata. Ripetizioni: {sequence_count}, Totale click: {self.click_count}")
            
            # Se abbiamo raggiunto il numero massimo di ripetizioni, ferma
            if sequence_count >= max_repeats and not self.infinite_sequence.get():
                self.root.after(0, self.stop_clicking)
                
        except Exception as e:
            self.log_message(f"[ERRORE CRITICO] Errore nel metodo execute_sequence: {str(e)}")
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
    
    # === METODI PER SEQUENZE E MACRO ===
    
    def toggle_execution_mode(self):
        """Cambia modalità di esecuzione tra singola e sequenza"""
        mode = self.execution_mode.get()
        self.sequence_mode = (mode == "sequence")
        
        if self.sequence_mode:
            self.log_message("Modalità sequenza attivata")
        else:
            self.log_message("Modalità click singoli attivata")
    
    def toggle_recording(self):
        """Avvia/ferma la registrazione macro"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Inizia la registrazione di una macro"""
        try:
            # Ferma prima qualsiasi registrazione in corso
            if self.is_recording:
                self.stop_recording()
            
            self.is_recording = True
            self.recorded_sequence = []
            self.record_button.config(text="⏹️ Ferma Registrazione")
            self.recording_status.set("🔴 REGISTRAZIONE IN CORSO - Clicca per registrare")
            
            # Rimuovi eventuali bind precedenti
            try:
                self.root.unbind('<Button-1>')
                self.root.unbind('<Button-2>')
                self.root.unbind('<Button-3>')
            except:
                pass  # Ignora se non ci sono bind da rimuovere
            
            # Bind click del mouse per registrazione
            self.root.bind('<Button-1>', self.record_click)
            self.root.bind('<Button-2>', self.record_click)
            self.root.bind('<Button-3>', self.record_click)
            
            self.log_message("Registrazione macro iniziata")
            
        except Exception as e:
            self.log_message(f"Errore nell'avviare la registrazione: {str(e)}")
            self.is_recording = False
            self.record_button.config(text="🔴 Inizia Registrazione")
            self.recording_status.set("Errore nella registrazione")
    
    def stop_recording(self):
        """Ferma la registrazione macro"""
        try:
            self.is_recording = False
            self.record_button.config(text="🔴 Inizia Registrazione")
            
            # Rimuovi bind in modo sicuro
            try:
                self.root.unbind('<Button-1>')
            except:
                pass
            try:
                self.root.unbind('<Button-2>')
            except:
                pass
            try:
                self.root.unbind('<Button-3>')
            except:
                pass
            
            # Aggiorna status e sequenza
            num_clicks = len(self.recorded_sequence) if hasattr(self, 'recorded_sequence') else 0
            self.recording_status.set(f"Registrazione completata - {num_clicks} click registrati")
            
            # Copia sequenza registrata in quella corrente
            if hasattr(self, 'recorded_sequence') and self.recorded_sequence:
                self.current_sequence = self.recorded_sequence.copy()
                self.update_sequence_display()
            
            self.log_message(f"Registrazione completata: {num_clicks} click")
            
        except Exception as e:
            self.log_message(f"Errore nel fermare la registrazione: {str(e)}")
            self.is_recording = False
            self.record_button.config(text="🔴 Inizia Registrazione")
            self.recording_status.set("Errore nel fermare la registrazione")
    
    def record_click(self, event):
        """Registra un click durante la registrazione macro con validazione robusta"""
        try:
            if not self.is_recording:
                return
            
            # Verifica che l'evento sia valido
            if not hasattr(event, 'num') or not hasattr(event, 'x') or not hasattr(event, 'y'):
                self.log_message("Evento click non valido ignorato")
                return
            
            # Determina tipo di click
            button_map = {1: 'left', 2: 'middle', 3: 'right'}
            button = button_map.get(event.num, 'left')
            
            # Ottieni posizione assoluta del mouse con validazione
            x, y = None, None
            try:
                import pyautogui
                x, y = pyautogui.position()
                
                # Verifica che le coordinate siano ragionevoli
                if x < 0 or y < 0 or x > 32767 or y > 32767:
                    raise ValueError(f"Coordinate fuori range: ({x}, {y})")
                    
            except Exception as pos_error:
                # Fallback alla posizione relativa alla finestra
                try:
                    x = self.root.winfo_rootx() + event.x
                    y = self.root.winfo_rooty() + event.y
                    
                    # Verifica anche il fallback
                    if x < 0 or y < 0 or x > 32767 or y > 32767:
                        self.log_message(f"Coordinate fallback non valide: ({x}, {y})")
                        return
                        
                except Exception:
                    self.log_message(f"Impossibile ottenere posizione mouse: {pos_error}")
                    return
            
            # Verifica che la sequenza non diventi troppo lunga
            if len(self.recorded_sequence) >= 1000:  # Limite di sicurezza
                self.log_message("Limite massimo sequenza raggiunto (1000 click)")
                self.stop_recording()
                return
            
            # Aggiungi alla sequenza
            click_data = {
                'x': int(x),
                'y': int(y),
                'button': button,
                'double': False,
                'delay': 1.0  # Delay di default
            }
            
            self.recorded_sequence.append(click_data)
            self.log_message(f"Click registrato: {button.upper()} in ({x}, {y})")
            
            # Aggiorna il contatore nella status
            num_clicks = len(self.recorded_sequence)
            self.recording_status.set(f"🔴 REGISTRAZIONE - {num_clicks} click registrati")
            
        except Exception as e:
            self.log_message(f"Errore durante registrazione click: {str(e)}")
            # Non fermare la registrazione per un singolo errore, ma logga l'errore
    
    def clear_sequence(self):
        """Cancella la sequenza corrente"""
        self.current_sequence = []
        self.recorded_sequence = []
        self.update_sequence_display()
        self.recording_status.set("Sequenza cancellata")
        self.log_message("Sequenza cancellata")
    
    def update_sequence_display(self):
        """Aggiorna la visualizzazione della sequenza"""
        self.sequence_listbox.delete(0, tk.END)
        
        for i, click in enumerate(self.current_sequence):
            button_text = click['button'].upper()
            double_text = " (DOPPIO)" if click.get('double', False) else ""
            delay_text = f" - Pausa: {click.get('delay', 1.0)}s"
            
            display_text = f"{i+1}. Click {button_text} in ({click['x']}, {click['y']}){double_text}{delay_text}"
            self.sequence_listbox.insert(tk.END, display_text)
    
    def add_manual_click(self):
        """Aggiunge un click manuale alla sequenza"""
        dialog = ClickDialog(self.root, "Aggiungi Click")
        if dialog.result:
            self.current_sequence.append(dialog.result)
            self.update_sequence_display()
            self.log_message(f"Click manuale aggiunto: {dialog.result['button'].upper()} in ({dialog.result['x']}, {dialog.result['y']})")
    
    def edit_selected_click(self):
        """Modifica il click selezionato"""
        selection = self.sequence_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona un click da modificare")
            return
        
        index = selection[0]
        current_click = self.current_sequence[index]
        
        dialog = ClickDialog(self.root, "Modifica Click", current_click)
        if dialog.result:
            self.current_sequence[index] = dialog.result
            self.update_sequence_display()
            self.log_message(f"Click modificato: {dialog.result['button'].upper()} in ({dialog.result['x']}, {dialog.result['y']})")
    
    def remove_selected_click(self):
        """Rimuove il click selezionato"""
        selection = self.sequence_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona un click da rimuovere")
            return
        
        index = selection[0]
        removed_click = self.current_sequence.pop(index)
        self.update_sequence_display()
        self.log_message(f"Click rimosso: {removed_click['button'].upper()} in ({removed_click['x']}, {removed_click['y']})")
    
    def toggle_infinite_sequence(self):
        """Abilita/disabilita sequenza infinita"""
        if self.infinite_sequence.get():
            self.log_message("Sequenza infinita abilitata")
        else:
            self.log_message("Sequenza infinita disabilitata")
    
    # === METODI PER PROFILI ===
    
    def get_current_config(self) -> Dict:
        """Ottiene la configurazione corrente"""
        config = {
            'basic_settings': {
                'min_interval': self.min_interval.get(),
                'max_interval': self.max_interval.get(),
                'infinite_clicks': self.infinite_clicks.get(),
                'max_clicks': self.max_clicks.get()
            },
            'advanced_settings': {
                'click_type': self.click_type.get(),
                'double_click': self.double_click.get(),
                'use_current_position': self.use_current_position.get(),
                'fixed_x': self.fixed_x.get(),
                'fixed_y': self.fixed_y.get(),
                'initial_delay': self.initial_delay.get(),
                'play_sound': self.play_sound.get(),
                'minimize_on_start': self.minimize_on_start.get()
            },
            'sequence_settings': {
                'execution_mode': self.execution_mode.get(),
                'current_sequence': self.current_sequence,
                'sequence_repeats': self.sequence_repeats.get(),
                'sequence_pause': self.sequence_pause.get(),
                'infinite_sequence': self.infinite_sequence.get()
            }
        }
        return config
    
    def apply_config(self, config: Dict):
        """Applica una configurazione con validazione"""
        try:
            # Validazione struttura generale
            if not isinstance(config, dict):
                raise ValueError("Configurazione deve essere un dizionario")
            
            # Impostazioni base con validazione
            basic = config.get('basic_settings', {})
            if not isinstance(basic, dict):
                raise ValueError("Sezione basic_settings non valida")
            
            # Validazione intervalli
            min_interval = str(basic.get('min_interval', '1'))
            max_interval = str(basic.get('max_interval', '5'))
            
            try:
                min_val = float(min_interval)
                max_val = float(max_interval)
                if min_val < 0.001 or min_val > 3600:  # 1ms - 1 ora
                    min_interval = '1'
                if max_val < 0.001 or max_val > 3600:
                    max_interval = '5'
                if min_val > max_val:
                    min_interval, max_interval = '1', '5'
            except (ValueError, TypeError):
                min_interval, max_interval = '1', '5'
            
            self.min_interval.set(min_interval)
            self.max_interval.set(max_interval)
            
            # Validazione click massimi
            max_clicks = str(basic.get('max_clicks', '100'))
            try:
                max_clicks_val = int(max_clicks)
                if max_clicks_val < 1 or max_clicks_val > 10000000:
                    max_clicks = '100'
            except (ValueError, TypeError):
                max_clicks = '100'
            
            self.infinite_clicks.set(bool(basic.get('infinite_clicks', True)))
            self.max_clicks.set(max_clicks)
            
            # Impostazioni avanzate con validazione
            advanced = config.get('advanced_settings', {})
            if not isinstance(advanced, dict):
                raise ValueError("Sezione advanced_settings non valida")
            
            # Validazione tipo click
            click_type = advanced.get('click_type', 'left')
            if click_type not in ['left', 'right', 'middle']:
                click_type = 'left'
            self.click_type.set(click_type)
            
            self.double_click.set(bool(advanced.get('double_click', False)))
            self.use_current_position.set(bool(advanced.get('use_current_position', True)))
            
            # Validazione coordinate fisse
            fixed_x = str(advanced.get('fixed_x', '100'))
            fixed_y = str(advanced.get('fixed_y', '100'))
            
            try:
                x_val = int(fixed_x)
                y_val = int(fixed_y)
                if x_val < 0 or x_val > 32767:
                    fixed_x = '100'
                if y_val < 0 or y_val > 32767:
                    fixed_y = '100'
            except (ValueError, TypeError):
                fixed_x, fixed_y = '100', '100'
            
            self.fixed_x.set(fixed_x)
            self.fixed_y.set(fixed_y)
            
            # Validazione delay iniziale
            initial_delay = str(advanced.get('initial_delay', '3'))
            try:
                delay_val = float(initial_delay)
                if delay_val < 0 or delay_val > 3600:  # max 1 ora
                    initial_delay = '3'
            except (ValueError, TypeError):
                initial_delay = '3'
            
            self.initial_delay.set(initial_delay)
            self.play_sound.set(bool(advanced.get('play_sound', False)))
            self.minimize_on_start.set(bool(advanced.get('minimize_on_start', False)))
            
            # Impostazioni sequenze con validazione
            sequence = config.get('sequence_settings', {})
            if not isinstance(sequence, dict):
                raise ValueError("Sezione sequence_settings non valida")
            
            # Validazione modalità esecuzione
            execution_mode = sequence.get('execution_mode', 'single')
            if execution_mode not in ['single', 'sequence']:
                execution_mode = 'single'
            self.execution_mode.set(execution_mode)
            
            # Validazione sequenza
            current_sequence = sequence.get('current_sequence', [])
            if isinstance(current_sequence, list):
                # Limita lunghezza sequenza
                if len(current_sequence) > 1000:
                    current_sequence = current_sequence[:1000]
                    self.log_message("Sequenza troncata a 1000 click per sicurezza")
                
                # Valida ogni click nella sequenza
                validated_sequence = []
                for i, click in enumerate(current_sequence):
                    if isinstance(click, dict):
                        # Valida campi obbligatori
                        if all(field in click for field in ['x', 'y', 'button']):
                            try:
                                # Valida coordinate
                                x = int(click['x'])
                                y = int(click['y'])
                                if 0 <= x <= 32767 and 0 <= y <= 32767:
                                    # Valida button
                                    button = click['button']
                                    if button in ['left', 'right', 'middle']:
                                        # Valida delay se presente
                                        delay = click.get('delay', 1.0)
                                        try:
                                            delay = float(delay)
                                            if delay < 0 or delay > 3600:
                                                delay = 1.0
                                        except (ValueError, TypeError):
                                            delay = 1.0
                                        
                                        validated_click = {
                                            'x': x,
                                            'y': y,
                                            'button': button,
                                            'double': bool(click.get('double', False)),
                                            'delay': delay
                                        }
                                        validated_sequence.append(validated_click)
                            except (ValueError, TypeError):
                                continue  # Salta click non validi
                
                self.current_sequence = validated_sequence
            else:
                self.current_sequence = []
            
            # Validazione ripetizioni sequenza
            sequence_repeats = str(sequence.get('sequence_repeats', '1'))
            try:
                repeats_val = int(sequence_repeats)
                if repeats_val < 1 or repeats_val > 100000:
                    sequence_repeats = '1'
            except (ValueError, TypeError):
                sequence_repeats = '1'
            
            # Validazione pausa sequenza
            sequence_pause = str(sequence.get('sequence_pause', '1.0'))
            try:
                pause_val = float(sequence_pause)
                if pause_val < 0 or pause_val > 3600:
                    sequence_pause = '1.0'
            except (ValueError, TypeError):
                sequence_pause = '1.0'
            
            self.sequence_repeats.set(sequence_repeats)
            self.sequence_pause.set(sequence_pause)
            self.infinite_sequence.set(bool(sequence.get('infinite_sequence', False)))
            
            # Aggiorna UI
            self.toggle_click_count()
            self.toggle_position_mode()
            self.toggle_execution_mode()
            self.toggle_infinite_sequence()
            self.update_sequence_display()
            
        except ValueError as e:
            self.log_message(f"Errore di validazione nella configurazione: {str(e)}")
            # Applica configurazione di default in caso di errore
            self.apply_default_config()
        except Exception as e:
            self.log_message(f"Errore imprevisto nell'applicare la configurazione: {str(e)}")
            self.apply_default_config()
    
    def apply_default_config(self):
        """Applica una configurazione di default sicura"""
        try:
            self.min_interval.set('1')
            self.max_interval.set('5')
            self.infinite_clicks.set(True)
            self.max_clicks.set('100')
            self.click_type.set('left')
            self.double_click.set(False)
            self.use_current_position.set(True)
            self.fixed_x.set('100')
            self.fixed_y.set('100')
            self.initial_delay.set('3')
            self.play_sound.set(False)
            self.minimize_on_start.set(False)
            self.execution_mode.set('single')
            self.current_sequence = []
            self.sequence_repeats.set('1')
            self.sequence_pause.set('1.0')
            self.infinite_sequence.set(False)
            
            # Aggiorna UI
            self.toggle_click_count()
            self.toggle_position_mode()
            self.toggle_execution_mode()
            self.toggle_infinite_sequence()
            self.update_sequence_display()
            
            self.log_message("Configurazione di default applicata")
        except Exception as e:
            self.log_message(f"Errore nell'applicare configurazione di default: {str(e)}")
    
    def save_profile(self):
        """Salva il profilo corrente"""
        name = tk.simpledialog.askstring("Salva Profilo", "Nome del profilo:")
        if not name:
            return
        
        # Validazione del nome profilo
        if len(name.strip()) == 0:
            messagebox.showerror("Errore", "Il nome del profilo non può essere vuoto")
            return
            
        # Rimuovi caratteri non validi per il nome file
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
        if not safe_name:
            messagebox.showerror("Errore", "Nome profilo non valido")
            return
        
        # Assicura che la directory esista
        if not os.path.exists(self.profiles_dir):
            try:
                os.makedirs(self.profiles_dir)
            except OSError as e:
                messagebox.showerror("Errore", f"Impossibile creare la directory dei profili: {e}")
                return
        
        config = self.get_current_config()
        config['profile_name'] = name
        config['created_date'] = datetime.datetime.now().isoformat()
        
        filename = f"{safe_name}.json"
        filepath = os.path.join(self.profiles_dir, filename)
        temp_filepath = os.path.join(self.profiles_dir, f".temp_{safe_name}.json")
        
        try:
            # Scrivi prima in un file temporaneo
            with open(temp_filepath, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            # Poi rinomina il file (operazione atomica)
            if os.path.exists(filepath):
                # Backup del file esistente
                backup_path = os.path.join(self.profiles_dir, f"{safe_name}.backup.json")
                try:
                    if os.path.exists(backup_path):
                        os.remove(backup_path)
                    os.rename(filepath, backup_path)
                except OSError:
                    pass  # Continua anche se il backup fallisce
            
            os.rename(temp_filepath, filepath)
            
            self.current_profile = name
            self.current_profile_var.set(f"Profilo corrente: {name}")
            self.refresh_profiles_list()
            self.log_message(f"Profilo '{name}' salvato")
            
        except json.JSONEncodeError as e:
            messagebox.showerror("Errore", f"Errore nella codifica JSON: {e}")
        except IOError as e:
            messagebox.showerror("Errore", f"Errore di I/O nel salvare il profilo: {e}")
        except OSError as e:
            messagebox.showerror("Errore", f"Errore di sistema nel salvare il profilo: {e}")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore imprevisto nel salvare il profilo: {str(e)}")
        finally:
            # Pulizia: rimuovi il file temporaneo se esiste ancora
            if os.path.exists(temp_filepath):
                try:
                    os.remove(temp_filepath)
                except:
                    pass
    
    def load_profile(self):
        """Carica un profilo da file"""
        filepath = filedialog.askopenfilename(
            title="Carica Profilo",
            initialdir=self.profiles_dir,
            filetypes=[("File JSON", "*.json"), ("Tutti i file", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            # Verifica che il file esista e sia leggibile
            if not os.path.exists(filepath):
                messagebox.showerror("Errore", "File non trovato")
                return
            
            if not os.path.isfile(filepath):
                messagebox.showerror("Errore", "Il percorso specificato non è un file")
                return
            
            # Verifica dimensione file (max 10MB per sicurezza)
            file_size = os.path.getsize(filepath)
            if file_size > 10 * 1024 * 1024:  # 10MB
                messagebox.showerror("Errore", "File troppo grande (max 10MB)")
                return
            
            if file_size == 0:
                messagebox.showerror("Errore", "File vuoto")
                return
            
            with open(filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validazione struttura JSON
            if not isinstance(config, dict):
                messagebox.showerror("Errore", "Struttura profilo non valida")
                return
            
            # Validazione campi obbligatori
            required_sections = ['basic_settings', 'advanced_settings', 'sequence_settings']
            for section in required_sections:
                if section not in config or not isinstance(config[section], dict):
                    messagebox.showerror("Errore", f"Sezione '{section}' mancante o non valida")
                    return
            
            self.apply_config(config)
            
            profile_name = config.get('profile_name', os.path.basename(filepath))
            # Sanitizza il nome del profilo
            profile_name = str(profile_name)[:100]  # Limita lunghezza
            
            self.current_profile = profile_name
            self.current_profile_var.set(f"Profilo corrente: {profile_name}")
            self.log_message(f"Profilo '{profile_name}' caricato")
            
        except json.JSONDecodeError as e:
            messagebox.showerror("Errore", f"File JSON non valido: {str(e)}")
        except UnicodeDecodeError as e:
            messagebox.showerror("Errore", f"Errore di codifica file: {str(e)}")
        except PermissionError:
            messagebox.showerror("Errore", "Permessi insufficienti per leggere il file")
        except IOError as e:
            messagebox.showerror("Errore", f"Errore di I/O: {str(e)}")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore imprevisto nel caricare il profilo: {str(e)}")
    
    def export_profile(self):
        """Esporta il profilo corrente"""
        filepath = filedialog.asksaveasfilename(
            title="Esporta Profilo",
            defaultextension=".json",
            filetypes=[("File JSON", "*.json"), ("Tutti i file", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            # Verifica che la directory di destinazione esista e sia scrivibile
            export_dir = os.path.dirname(filepath)
            if not os.path.exists(export_dir):
                messagebox.showerror("Errore", "Directory di destinazione non esistente")
                return
            
            if not os.access(export_dir, os.W_OK):
                messagebox.showerror("Errore", "Permessi insufficienti per scrivere nella directory")
                return
            
            # Verifica che il nome file sia valido
            filename = os.path.basename(filepath)
            if not filename or filename.startswith('.'):
                messagebox.showerror("Errore", "Nome file non valido")
                return
            
            config = self.get_current_config()
            
            # Validazione della configurazione prima dell'esportazione
            if not isinstance(config, dict):
                messagebox.showerror("Errore", "Configurazione corrente non valida")
                return
            
            # Sanitizza il nome del profilo
            profile_name = self.current_profile or "Profilo Esportato"
            profile_name = str(profile_name)[:100]  # Limita lunghezza
            
            config['profile_name'] = profile_name
            config['exported_date'] = datetime.datetime.now().isoformat()
            
            # Verifica se il file esiste già
            if os.path.exists(filepath):
                if not messagebox.askyesno("Conferma", f"Il file '{filename}' esiste già. Sovrascrivere?"):
                    return
            
            # Scrivi con file temporaneo per sicurezza
            temp_filepath = filepath + ".tmp"
            
            try:
                with open(temp_filepath, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                
                # Operazione atomica
                if os.path.exists(filepath):
                    os.remove(filepath)
                os.rename(temp_filepath, filepath)
                
                self.log_message(f"Profilo esportato in: {filepath}")
                
            finally:
                # Pulizia file temporaneo
                if os.path.exists(temp_filepath):
                    try:
                        os.remove(temp_filepath)
                    except:
                        pass
            
        except json.JSONEncodeError as e:
            messagebox.showerror("Errore", f"Errore nella codifica JSON: {str(e)}")
        except PermissionError:
            messagebox.showerror("Errore", "Permessi insufficienti per scrivere il file")
        except IOError as e:
            messagebox.showerror("Errore", f"Errore di I/O: {str(e)}")
        except OSError as e:
            messagebox.showerror("Errore", f"Errore di sistema: {str(e)}")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore imprevisto nell'esportare il profilo: {str(e)}")
    
    def import_profile(self):
        """Importa un profilo da file esterno"""
        filepath = filedialog.askopenfilename(
            title="Importa Profilo",
            filetypes=[("File JSON", "*.json"), ("Tutti i file", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            # Verifica sicurezza del file
            if not os.path.exists(filepath):
                messagebox.showerror("Errore", "File non trovato")
                return
            
            if not os.path.isfile(filepath):
                messagebox.showerror("Errore", "Il percorso specificato non è un file")
                return
            
            # Verifica dimensione file (max 10MB)
            file_size = os.path.getsize(filepath)
            if file_size > 10 * 1024 * 1024:  # 10MB
                messagebox.showerror("Errore", "File troppo grande (max 10MB)")
                return
            
            if file_size == 0:
                messagebox.showerror("Errore", "File vuoto")
                return
            
            with open(filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validazione struttura JSON
            if not isinstance(config, dict):
                messagebox.showerror("Errore", "Struttura profilo non valida")
                return
            
            # Validazione campi obbligatori
            required_sections = ['basic_settings', 'advanced_settings', 'sequence_settings']
            for section in required_sections:
                if section not in config or not isinstance(config[section], dict):
                    messagebox.showerror("Errore", f"Sezione '{section}' mancante o non valida nel file")
                    return
            
            # Validazione sequenza se presente
            sequence_data = config.get('sequence_settings', {}).get('current_sequence', [])
            if sequence_data and isinstance(sequence_data, list):
                if len(sequence_data) > 1000:  # Limite di sicurezza
                    messagebox.showerror("Errore", "Sequenza troppo lunga (max 1000 click)")
                    return
                
                # Valida ogni click nella sequenza
                for i, click in enumerate(sequence_data):
                    if not isinstance(click, dict):
                        messagebox.showerror("Errore", f"Click {i+1} nella sequenza non valido")
                        return
                    
                    required_click_fields = ['x', 'y', 'button']
                    for field in required_click_fields:
                        if field not in click:
                            messagebox.showerror("Errore", f"Campo '{field}' mancante nel click {i+1}")
                            return
            
            # Chiedi nome per il profilo importato
            default_name = config.get('profile_name', 'Profilo Importato')
            # Sanitizza il nome di default
            default_name = str(default_name)[:50]  # Limita lunghezza
            
            name = tk.simpledialog.askstring(
                "Importa Profilo", 
                "Nome per il profilo importato:",
                initialvalue=default_name
            )
            
            if not name:
                return
            
            # Validazione nome profilo
            if len(name.strip()) == 0:
                messagebox.showerror("Errore", "Il nome del profilo non può essere vuoto")
                return
            
            if len(name) > 100:
                messagebox.showerror("Errore", "Nome profilo troppo lungo (max 100 caratteri)")
                return
            
            # Salva nella directory profili
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
            if not safe_name:
                messagebox.showerror("Errore", "Nome profilo non valido")
                return
            
            filename = f"{safe_name}.json"
            new_filepath = os.path.join(self.profiles_dir, filename)
            
            # Verifica se il file esiste già
            if os.path.exists(new_filepath):
                if not messagebox.askyesno("Conferma", f"Il profilo '{name}' esiste già. Sovrascrivere?"):
                    return
            
            config['profile_name'] = name
            config['imported_date'] = datetime.datetime.now().isoformat()
            
            # Scrivi con file temporaneo per sicurezza
            temp_filepath = os.path.join(self.profiles_dir, f".temp_{safe_name}.json")
            
            try:
                with open(temp_filepath, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                
                # Operazione atomica
                if os.path.exists(new_filepath):
                    os.remove(new_filepath)
                os.rename(temp_filepath, new_filepath)
                
                self.refresh_profiles_list()
                self.log_message(f"Profilo '{name}' importato")
                
            finally:
                # Pulizia file temporaneo
                if os.path.exists(temp_filepath):
                    try:
                        os.remove(temp_filepath)
                    except:
                        pass
            
        except json.JSONDecodeError as e:
            messagebox.showerror("Errore", f"File JSON non valido: {str(e)}")
        except UnicodeDecodeError as e:
            messagebox.showerror("Errore", f"Errore di codifica file: {str(e)}")
        except PermissionError:
            messagebox.showerror("Errore", "Permessi insufficienti per accedere al file")
        except IOError as e:
            messagebox.showerror("Errore", f"Errore di I/O: {str(e)}")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore imprevisto nell'importare il profilo: {str(e)}")
    
    def refresh_profiles_list(self):
        """Aggiorna la lista dei profili disponibili"""
        self.profiles_listbox.delete(0, tk.END)
        
        # Assicura che la directory esista
        if not os.path.exists(self.profiles_dir):
            try:
                os.makedirs(self.profiles_dir)
            except OSError as e:
                self.log_message(f"Errore creazione directory profili: {e}")
                return
        
        try:
            files = os.listdir(self.profiles_dir)
        except OSError as e:
            self.log_message(f"Errore lettura directory profili: {e}")
            return
        
        for filename in files:
            if not filename.endswith('.json'):
                continue
                
            filepath = os.path.join(self.profiles_dir, filename)
            
            # Verifica che sia un file e non una directory
            if not os.path.isfile(filepath):
                continue
            
            try:
                # Verifica dimensione file
                if os.path.getsize(filepath) == 0:
                    self.profiles_listbox.insert(tk.END, f"{filename[:-5]} (File vuoto)")
                    continue
                
                # Verifica che il file sia un JSON valido
                with open(filepath, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Verifica struttura base del profilo
                if not isinstance(config, dict):
                    self.profiles_listbox.insert(tk.END, f"{filename[:-5]} (Struttura invalida)")
                    continue
                
                profile_name = config.get('profile_name', filename[:-5])
                created_date = config.get('created_date', 'Data sconosciuta')
                
                if created_date != 'Data sconosciuta':
                    try:
                        date_obj = datetime.datetime.fromisoformat(created_date)
                        date_str = date_obj.strftime('%d/%m/%Y %H:%M')
                    except (ValueError, TypeError):
                        date_str = 'Data sconosciuta'
                else:
                    date_str = created_date
                
                display_text = f"{profile_name} ({date_str})"
                self.profiles_listbox.insert(tk.END, display_text)
                
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                self.profiles_listbox.insert(tk.END, f"{filename[:-5]} (File corrotto)")
                self.log_message(f"File profilo corrotto: {filename} - {e}")
            except (IOError, OSError) as e:
                self.profiles_listbox.insert(tk.END, f"{filename[:-5]} (Errore lettura)")
                self.log_message(f"Errore lettura profilo: {filename} - {e}")
            except Exception as e:
                self.profiles_listbox.insert(tk.END, f"{filename[:-5]} (Errore sconosciuto)")
                self.log_message(f"Errore imprevisto con profilo: {filename} - {e}")
    
    def load_selected_profile(self, event=None):
        """Carica il profilo selezionato dalla lista"""
        selection = self.profiles_listbox.curselection()
        if not selection:
            return
        
        selected_text = self.profiles_listbox.get(selection[0])
        profile_name = selected_text.split(' (')[0]  # Rimuovi la data
        
        # Trova il file corrispondente
        for filename in os.listdir(self.profiles_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.profiles_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    if config.get('profile_name', filename[:-5]) == profile_name:
                        self.apply_config(config)
                        self.current_profile = profile_name
                        self.current_profile_var.set(f"Profilo corrente: {profile_name}")
                        self.log_message(f"Profilo '{profile_name}' caricato")
                        return
                        
                except Exception as e:
                    continue
        
        messagebox.showerror("Errore", "Profilo non trovato o corrotto")
    
    def delete_selected_profile(self):
        """Elimina il profilo selezionato"""
        selection = self.profiles_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona un profilo da eliminare")
            return
        
        selected_text = self.profiles_listbox.get(selection[0])
        profile_name = selected_text.split(' (')[0]
        
        if not messagebox.askyesno("Conferma", f"Eliminare il profilo '{profile_name}'?"):
            return
        
        # Trova e elimina il file
        for filename in os.listdir(self.profiles_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.profiles_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    if config.get('profile_name', filename[:-5]) == profile_name:
                        os.remove(filepath)
                        self.refresh_profiles_list()
                        self.log_message(f"Profilo '{profile_name}' eliminato")
                        
                        if self.current_profile == profile_name:
                            self.current_profile = None
                            self.current_profile_var.set("Nessun profilo caricato")
                        return
                        
                except Exception as e:
                    continue
        
        messagebox.showerror("Errore", "Profilo non trovato")
    
    def duplicate_selected_profile(self):
        """Duplica il profilo selezionato"""
        selection = self.profiles_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona un profilo da duplicare")
            return
        
        selected_text = self.profiles_listbox.get(selection[0])
        original_name = selected_text.split(' (')[0]
        
        new_name = tk.simpledialog.askstring(
            "Duplica Profilo", 
            "Nome per il profilo duplicato:",
            initialvalue=f"{original_name} - Copia"
        )
        
        if not new_name:
            return
        
        # Trova il file originale
        for filename in os.listdir(self.profiles_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.profiles_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    if config.get('profile_name', filename[:-5]) == original_name:
                        # Crea il duplicato
                        config['profile_name'] = new_name
                        config['created_date'] = datetime.datetime.now().isoformat()
                        config['duplicated_from'] = original_name
                        
                        safe_name = "".join(c for c in new_name if c.isalnum() or c in (' ', '-', '_')).strip()
                        new_filename = f"{safe_name}.json"
                        new_filepath = os.path.join(self.profiles_dir, new_filename)
                        
                        with open(new_filepath, 'w', encoding='utf-8') as f:
                            json.dump(config, f, indent=2, ensure_ascii=False)
                        
                        self.refresh_profiles_list()
                        self.log_message(f"Profilo '{new_name}' creato come copia di '{original_name}'")
                        return
                        
                except Exception as e:
                    continue
        
        messagebox.showerror("Errore", "Profilo originale non trovato")
    
    def load_preset_profile(self, preset_type: str):
        """Carica un profilo predefinito"""
        presets = {
            'gaming': {
                'profile_name': 'Gaming - Click Rapidi',
                'basic_settings': {
                    'min_interval': '0.1',
                    'max_interval': '0.5',
                    'infinite_clicks': True,
                    'max_clicks': '1000'
                },
                'advanced_settings': {
                    'click_type': 'left',
                    'double_click': False,
                    'use_current_position': True,
                    'fixed_x': '500',
                    'fixed_y': '300',
                    'initial_delay': '3',
                    'play_sound': False,
                    'minimize_on_start': True
                },
                'sequence_settings': {
                    'execution_mode': 'single',
                    'current_sequence': [],
                    'sequence_repeats': '1',
                    'sequence_pause': '0.5',
                    'infinite_sequence': False
                }
            },
            'office': {
                'profile_name': 'Ufficio - Click Lenti',
                'basic_settings': {
                    'min_interval': '2.0',
                    'max_interval': '5.0',
                    'infinite_clicks': False,
                    'max_clicks': '50'
                },
                'advanced_settings': {
                    'click_type': 'left',
                    'double_click': False,
                    'use_current_position': True,
                    'fixed_x': '400',
                    'fixed_y': '400',
                    'initial_delay': '5',
                    'play_sound': True,
                    'minimize_on_start': False
                },
                'sequence_settings': {
                    'execution_mode': 'single',
                    'current_sequence': [],
                    'sequence_repeats': '1',
                    'sequence_pause': '2.0',
                    'infinite_sequence': False
                }
            },
            'test': {
                'profile_name': 'Test - Click Medi',
                'basic_settings': {
                    'min_interval': '1.0',
                    'max_interval': '3.0',
                    'infinite_clicks': False,
                    'max_clicks': '10'
                },
                'advanced_settings': {
                    'click_type': 'left',
                    'double_click': False,
                    'use_current_position': False,
                    'fixed_x': '300',
                    'fixed_y': '300',
                    'initial_delay': '3',
                    'play_sound': True,
                    'minimize_on_start': False
                },
                'sequence_settings': {
                    'execution_mode': 'single',
                    'current_sequence': [],
                    'sequence_repeats': '1',
                    'sequence_pause': '1.0',
                    'infinite_sequence': False
                }
            }
        }
        
        if preset_type in presets:
            config = presets[preset_type]
            self.apply_config(config)
            self.current_profile = config['profile_name']
            self.current_profile_var.set(f"Profilo corrente: {config['profile_name']}")
            self.log_message(f"Profilo predefinito '{config['profile_name']}' caricato")
    
    def on_closing(self):
        """Gestisce la chiusura dell'applicazione in modo sicuro"""
        try:
            # Ferma la registrazione se attiva
            if hasattr(self, 'is_recording') and self.is_recording:
                try:
                    self.stop_recording()
                except Exception as e:
                    self.log_message(f"Errore fermando registrazione: {e}")
            
            # Ferma i click se attivi
            if hasattr(self, 'is_running') and self.is_running:
                if messagebox.askokcancel("Chiusura", 
                                        "I click sono ancora attivi. Vuoi fermarli e chiudere?"):
                    try:
                        self.stop_clicking()
                        
                        # Attendi che il thread si fermi con timeout
                        if hasattr(self, 'click_thread') and self.click_thread and self.click_thread.is_alive():
                            self.click_thread.join(timeout=3.0)
                            if self.click_thread.is_alive():
                                self.log_message("[AVVISO] Thread di click non terminato entro il timeout")
                                
                    except Exception as e:
                        self.log_message(f"Errore fermando click: {e}")
                else:
                    return  # Non chiudere se l'utente annulla
            
            # Rimuovi tutti i bind degli eventi in modo sicuro
            event_bindings = ['<Button-1>', '<Button-2>', '<Button-3>', '<KeyPress>', '<KeyRelease>']
            for binding in event_bindings:
                try:
                    self.root.unbind(binding)
                except Exception:
                    pass  # Ignora se il binding non esiste
            
            # Salva stato dell'applicazione se necessario
            try:
                # Qui potresti salvare configurazioni o stato dell'app
                pass
            except Exception as e:
                self.log_message(f"Errore salvando stato: {e}")
            
            # Chiudi l'applicazione
            self.root.quit()  # Usa quit() invece di destroy() per una chiusura più pulita
            self.root.destroy()
            
        except Exception as e:
            print(f"Errore critico durante la chiusura: {e}")
            # Forza la chiusura in caso di errore critico
            try:
                import os
                import signal
                os.kill(os.getpid(), signal.SIGTERM)
            except Exception:
                try:
                    self.root.destroy()
                except Exception:
                    import sys
                    sys.exit(1)


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