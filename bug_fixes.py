#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correzioni di Bug per Mouse Auto Clicker
Autore: Assistant AI
Descrizione: Correzioni per problemi identificati nel codice
"""

# PROBLEMI IDENTIFICATI E CORREZIONI:

# 1. PROBLEMA: Metodo play_notification_sound usa winsound su macOS
# CORREZIONE: Migliorare la gestione multi-piattaforma
def play_notification_sound_fixed(self):
    """Riproduce un suono di notifica (se abilitato) - VERSIONE CORRETTA"""
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

# 2. PROBLEMA: Gestione non sicura dei file nei metodi di profilo
# CORREZIONE: Aggiungere controlli di esistenza e validazione
def refresh_profiles_list_fixed(self):
    """Aggiorna la lista dei profili disponibili - VERSIONE CORRETTA"""
    self.profiles_listbox.delete(0, tk.END)
    
    try:
        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir)
            return
            
        for filename in os.listdir(self.profiles_dir):
            if not filename.endswith('.json'):
                continue
                
            filepath = os.path.join(self.profiles_dir, filename)
            
            # Verifica che sia un file e non una directory
            if not os.path.isfile(filepath):
                continue
                
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Validazione struttura JSON
                if not isinstance(config, dict):
                    raise ValueError("Struttura JSON non valida")
                
                profile_name = config.get('profile_name', filename[:-5])
                created_date = config.get('created_date', 'Data sconosciuta')
                
                if created_date != 'Data sconosciuta':
                    try:
                        import datetime
                        date_obj = datetime.datetime.fromisoformat(created_date)
                        date_str = date_obj.strftime('%d/%m/%Y %H:%M')
                    except (ValueError, TypeError):
                        date_str = 'Data sconosciuta'
                else:
                    date_str = created_date
                
                display_text = f"{profile_name} ({date_str})"
                self.profiles_listbox.insert(tk.END, display_text)
                
            except (json.JSONDecodeError, ValueError, IOError) as e:
                # File corrotto o non leggibile
                self.profiles_listbox.insert(tk.END, f"{filename[:-5]} (File corrotto)")
                self.log_message(f"File profilo corrotto: {filename} - {str(e)}")
    
    except Exception as e:
        self.log_message(f"Errore nell'aggiornare la lista profili: {str(e)}")

# 3. PROBLEMA: Validazione insufficiente nei metodi di configurazione
# CORREZIONE: Aggiungere validazioni più robuste
def validate_configuration_enhanced(self):
    """Valida tutta la configurazione prima di iniziare - VERSIONE MIGLIORATA"""
    # Valida intervalli
    min_val, max_val = self.validate_intervals()
    if min_val is None:
        return False
    
    # Validazione aggiuntiva per intervalli estremi
    if min_val > 3600 or max_val > 3600:  # Più di 1 ora
        if not messagebox.askyesno("Attenzione", 
                                  "Hai impostato intervalli molto lunghi (>1 ora). Continuare?"):
            return False
    
    # Valida numero massimo click se non infiniti
    if not self.infinite_clicks.get():
        try:
            max_clicks = int(self.max_clicks.get())
            if max_clicks <= 0:
                raise ValueError("Il numero massimo di click deve essere maggiore di 0")
            if max_clicks > 1000000:  # Limite ragionevole
                if not messagebox.askyesno("Attenzione", 
                                          f"Hai impostato {max_clicks} click. Continuare?"):
                    return False
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
            
            # Verifica che le coordinate siano entro i limiti dello schermo
            import pyautogui
            screen_width, screen_height = pyautogui.size()
            if x >= screen_width or y >= screen_height:
                if not messagebox.askyesno("Attenzione", 
                                          f"Le coordinate ({x}, {y}) sono fuori dallo schermo. Continuare?"):
                    return False
        except ValueError:
            messagebox.showerror("Errore", "Inserisci coordinate valide")
            return False
    
    # Valida ritardo iniziale
    try:
        delay = float(self.initial_delay.get())
        if delay < 0:
            raise ValueError("Il ritardo iniziale deve essere positivo")
        if delay > 3600:  # Più di 1 ora
            if not messagebox.askyesno("Attenzione", 
                                      f"Ritardo iniziale di {delay} secondi. Continuare?"):
                return False
    except ValueError:
        messagebox.showerror("Errore", "Inserisci un ritardo iniziale valido")
        return False
    
    # Valida sequenza se in modalità sequenza
    if hasattr(self, 'sequence_mode') and self.sequence_mode:
        if not hasattr(self, 'current_sequence') or not self.current_sequence:
            messagebox.showerror("Errore", "Nessuna sequenza definita per la modalità sequenza")
            return False
        
        # Valida parametri sequenza
        try:
            if not self.infinite_sequence.get():
                repeats = int(self.sequence_repeats.get())
                if repeats <= 0:
                    raise ValueError("Il numero di ripetizioni deve essere maggiore di 0")
            
            pause = float(self.sequence_pause.get())
            if pause < 0:
                raise ValueError("La pausa tra sequenze deve essere positiva")
        except ValueError as e:
            messagebox.showerror("Errore", f"Parametri sequenza non validi: {str(e)}")
            return False
    
    return True

# 4. PROBLEMA: Gestione thread non sicura
# CORREZIONE: Migliorare la gestione dei thread
def stop_clicking_safe(self):
    """Ferma il ciclo di click automatici in modo sicuro - VERSIONE MIGLIORATA"""
    self.is_running = False
    
    # Attendi che il thread finisca (con timeout)
    if hasattr(self, 'click_thread') and self.click_thread and self.click_thread.is_alive():
        self.click_thread.join(timeout=2.0)  # Attendi max 2 secondi
        if self.click_thread.is_alive():
            self.log_message("[AVVISO] Il thread di click non si è fermato entro il timeout")
    
    self.start_button.config(state='normal')
    self.stop_button.config(state='disabled')
    self.status_var.set("Fermato")
    
    # Ripristina finestra se era minimizzata
    try:
        if self.root.state() == 'iconic':
            self.root.deiconify()
    except tk.TclError:
        pass  # Finestra potrebbe essere già chiusa
    
    self.log_message("Click automatici fermati")
    
    # Suono di stop
    try:
        self.play_notification_sound()
    except Exception as e:
        self.log_message(f"Errore nel suono di notifica: {str(e)}")

# 5. PROBLEMA: Mancanza di validazione input in ClickDialog
# CORREZIONE: Aggiungere validazioni più robuste
def ok_clicked_enhanced(self):
    """Gestisce il click su OK - VERSIONE MIGLIORATA"""
    try:
        # Valida i dati
        x_str = self.x_var.get().strip()
        y_str = self.y_var.get().strip()
        delay_str = self.delay_var.get().strip()
        
        if not x_str or not y_str or not delay_str:
            raise ValueError("Tutti i campi devono essere compilati")
        
        x = int(x_str)
        y = int(y_str)
        delay = float(delay_str)
        
        # Validazioni aggiuntive
        if x < 0 or y < 0:
            raise ValueError("Le coordinate devono essere positive")
        
        if x > 9999 or y > 9999:
            raise ValueError("Le coordinate sono troppo grandi")
        
        if delay < 0:
            raise ValueError("Il delay non può essere negativo")
        
        if delay > 3600:
            raise ValueError("Il delay non può essere maggiore di 1 ora")
        
        # Verifica coordinate entro schermo
        try:
            import pyautogui
            screen_width, screen_height = pyautogui.size()
            if x >= screen_width or y >= screen_height:
                import tkinter.messagebox as mb
                if not mb.askyesno("Attenzione", 
                                  f"Le coordinate ({x}, {y}) sono fuori dallo schermo. Continuare?"):
                    return
        except Exception:
            pass  # Se non riesce a verificare, continua
        
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
        import tkinter.messagebox as mb
        mb.showerror("Errore", f"Dati non validi: {str(e)}")
    except Exception as e:
        import tkinter.messagebox as mb
        mb.showerror("Errore", f"Errore imprevisto: {str(e)}")

# 6. PROBLEMA: Gestione file non sicura nei metodi di import/export
# CORREZIONE: Aggiungere validazioni e gestione errori
def save_profile_safe(self):
    """Salva il profilo corrente in modo sicuro - VERSIONE MIGLIORATA"""
    import tkinter.simpledialog as sd
    import tkinter.messagebox as mb
    
    name = sd.askstring("Salva Profilo", "Nome del profilo:")
    if not name:
        return
    
    # Validazione nome
    name = name.strip()
    if not name:
        mb.showerror("Errore", "Il nome del profilo non può essere vuoto")
        return
    
    if len(name) > 100:
        mb.showerror("Errore", "Il nome del profilo è troppo lungo (max 100 caratteri)")
        return
    
    # Rimuovi caratteri non validi per il nome file
    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_', '.')).strip()
    if not safe_name:
        mb.showerror("Errore", "Nome profilo non valido")
        return
    
    # Verifica che la directory esista
    if not os.path.exists(self.profiles_dir):
        try:
            os.makedirs(self.profiles_dir)
        except OSError as e:
            mb.showerror("Errore", f"Impossibile creare la directory profili: {str(e)}")
            return
    
    filename = f"{safe_name}.json"
    filepath = os.path.join(self.profiles_dir, filename)
    
    # Verifica se il file esiste già
    if os.path.exists(filepath):
        if not mb.askyesno("Conferma", f"Il profilo '{name}' esiste già. Sovrascrivere?"):
            return
    
    try:
        config = self.get_current_config()
        config['profile_name'] = name
        config['created_date'] = datetime.datetime.now().isoformat()
        
        # Validazione configurazione prima del salvataggio
        if not isinstance(config, dict):
            raise ValueError("Configurazione non valida")
        
        # Salvataggio atomico (scrivi in file temporaneo poi rinomina)
        temp_filepath = filepath + '.tmp'
        with open(temp_filepath, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        # Rinomina solo se la scrittura è riuscita
        os.rename(temp_filepath, filepath)
        
        self.current_profile = name
        self.current_profile_var.set(f"Profilo corrente: {name}")
        self.refresh_profiles_list()
        self.log_message(f"Profilo '{name}' salvato")
        
    except Exception as e:
        # Pulisci file temporaneo se esiste
        temp_filepath = filepath + '.tmp'
        if os.path.exists(temp_filepath):
            try:
                os.remove(temp_filepath)
            except:
                pass
        
        mb.showerror("Errore", f"Errore nel salvare il profilo: {str(e)}")
        self.log_message(f"Errore nel salvare il profilo '{name}': {str(e)}")

# ISTRUZIONI PER APPLICARE LE CORREZIONI:
"""
Per applicare queste correzioni al file mouse_clicker.py:

1. Sostituire il metodo play_notification_sound con play_notification_sound_fixed
2. Sostituire il metodo refresh_profiles_list con refresh_profiles_list_fixed
3. Sostituire il metodo validate_configuration con validate_configuration_enhanced
4. Sostituire il metodo stop_clicking con stop_clicking_safe
5. Sostituire il metodo ok_clicked in ClickDialog con ok_clicked_enhanced
6. Sostituire il metodo save_profile con save_profile_safe

Queste correzioni risolvono:
- Problemi di compatibilità multi-piattaforma
- Gestione non sicura dei file
- Validazioni insufficienti
- Race conditions nei thread
- Mancanza di controlli sui limiti
- Gestione errori migliorata
"""