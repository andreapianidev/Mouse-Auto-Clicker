#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility per testare la finestra di licenza su macOS
Autore: Andrea Piani
Descrizione: Permette di testare la finestra di licenza anche con licenza già attivata
"""

import os
import json
import tkinter as tk
from tkinter import messagebox, ttk
from license_manager import LicenseManager, LicenseDialog
import shutil
from datetime import datetime

class LicenseTestManager:
    """Manager per testare la finestra di licenza"""
    
    def __init__(self):
        self.license_file = "license_data.json"
        self.backup_file = "license_data_backup.json"
        self.original_data = None
        
    def backup_license_data(self):
        """Crea un backup dei dati di licenza attuali"""
        if os.path.exists(self.license_file):
            try:
                with open(self.license_file, 'r', encoding='utf-8') as f:
                    self.original_data = json.load(f)
                
                # Crea backup fisico
                shutil.copy2(self.license_file, self.backup_file)
                return True
            except Exception as e:
                print(f"Errore nel backup: {e}")
                return False
        return True
    
    def create_test_license_data(self, uses_count=4):
        """Crea dati di licenza temporanei per il test"""
        test_data = {
            'device_id': 'test-device-12345678',
            'uses_count': uses_count,
            'first_use_date': datetime.now().isoformat(),
            'premium_license': False,
            'license_key': None,
            'license_date': None
        }
        
        try:
            with open(self.license_file, 'w', encoding='utf-8') as f:
                json.dump(test_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Errore nella creazione dati test: {e}")
            return False
    
    def restore_license_data(self):
        """Ripristina i dati di licenza originali"""
        try:
            if os.path.exists(self.backup_file):
                shutil.copy2(self.backup_file, self.license_file)
                os.remove(self.backup_file)
            elif self.original_data:
                with open(self.license_file, 'w', encoding='utf-8') as f:
                    json.dump(self.original_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Errore nel ripristino: {e}")
            return False

class LicenseTestApp:
    """Applicazione per testare la finestra di licenza"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Test Finestra Licenza - macOS")
        self.root.geometry("500x400")
        
        # Centra la finestra
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (250)
        y = (self.root.winfo_screenheight() // 2) - (200)
        self.root.geometry(f"500x400+{x}+{y}")
        
        self.test_manager = LicenseTestManager()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura l'interfaccia utente"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titolo
        title_label = ttk.Label(main_frame, 
                               text="Test Finestra Licenza Premium",
                               font=('SF Pro Display', 18, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Descrizione
        desc_text = ("Questa utility ti permette di testare la finestra di licenza\n"
                    "anche se hai già acquistato la licenza premium.\n\n"
                    "I tuoi dati di licenza originali verranno salvati\n"
                    "e ripristinati automaticamente dopo il test.")
        
        desc_label = ttk.Label(main_frame, text=desc_text, 
                              font=('SF Pro Display', 12),
                              justify=tk.CENTER)
        desc_label.pack(pady=(0, 30))
        
        # Frame per i pulsanti di test
        test_frame = ttk.LabelFrame(main_frame, text="Opzioni di Test", padding="15")
        test_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Test con 4 utilizzi (mostra finestra limite)
        test4_button = ttk.Button(test_frame, 
                                 text="Test con 4 utilizzi (1 rimasto)",
                                 command=lambda: self.run_test(4))
        test4_button.pack(fill=tk.X, pady=(0, 10))
        
        # Test con 5 utilizzi (mostra finestra acquisto)
        test5_button = ttk.Button(test_frame, 
                                 text="Test con 5 utilizzi (limite raggiunto)",
                                 command=lambda: self.run_test(5))
        test5_button.pack(fill=tk.X, pady=(0, 10))
        
        # Test con 0 utilizzi (primo avvio)
        test0_button = ttk.Button(test_frame, 
                                 text="Test primo avvio (0 utilizzi)",
                                 command=lambda: self.run_test(0))
        test0_button.pack(fill=tk.X)
        
        # Frame per controlli
        control_frame = ttk.LabelFrame(main_frame, text="Controlli", padding="15")
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Pulsante per vedere stato attuale
        status_button = ttk.Button(control_frame, 
                                  text="Mostra Stato Licenza Attuale",
                                  command=self.show_current_status)
        status_button.pack(fill=tk.X, pady=(0, 10))
        
        # Pulsante per ripristinare
        restore_button = ttk.Button(control_frame, 
                                   text="Ripristina Dati Originali",
                                   command=self.restore_original_data)
        restore_button.pack(fill=tk.X)
        
        # Frame per uscita
        exit_frame = ttk.Frame(main_frame)
        exit_frame.pack(fill=tk.X, pady=(20, 0))
        
        exit_button = ttk.Button(exit_frame, text="Esci", command=self.root.quit)
        exit_button.pack(side=tk.RIGHT)
        
    def run_test(self, uses_count):
        """Esegue un test con il numero di utilizzi specificato"""
        # Backup dati originali
        if not self.test_manager.backup_license_data():
            messagebox.showerror("Errore", "Impossibile creare backup dei dati")
            return
        
        # Crea dati di test
        if not self.test_manager.create_test_license_data(uses_count):
            messagebox.showerror("Errore", "Impossibile creare dati di test")
            return
        
        try:
            # Crea license manager con dati di test
            license_manager = LicenseManager()
            
            # Mostra informazioni pre-test
            remaining = license_manager.get_remaining_uses()
            can_use = license_manager.can_use_app()
            
            info_msg = (f"Stato test:\n"
                       f"Utilizzi: {uses_count}/5\n"
                       f"Rimanenti: {remaining}\n"
                       f"Può usare app: {can_use}\n\n"
                       f"Ora verrà mostrata la finestra di licenza...")
            
            messagebox.showinfo("Test Avviato", info_msg)
            
            # Apri finestra di licenza
            if not can_use:
                dialog = LicenseDialog(self.root, license_manager)
                messagebox.showinfo("Test Completato", 
                                   f"Risultato dialog: {dialog.result}")
            else:
                # Simula incremento utilizzo e controlla
                license_manager.increment_usage()
                if not license_manager.can_use_app():
                    dialog = LicenseDialog(self.root, license_manager)
                    messagebox.showinfo("Test Completato", 
                                       f"Risultato dialog: {dialog.result}")
                else:
                    messagebox.showinfo("Test", "L'app può ancora essere utilizzata")
            
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante il test: {str(e)}")
        
        finally:
            # Ripristina sempre i dati originali
            self.test_manager.restore_license_data()
            messagebox.showinfo("Ripristino", "Dati originali ripristinati")
    
    def show_current_status(self):
        """Mostra lo stato attuale della licenza"""
        try:
            license_manager = LicenseManager()
            
            status_msg = (f"Stato Licenza Attuale:\n\n"
                         f"Device ID: {license_manager.license_data['device_id'][:8]}...\n"
                         f"Utilizzi: {license_manager.license_data['uses_count']}/5\n"
                         f"Rimanenti: {license_manager.get_remaining_uses()}\n"
                         f"Premium: {license_manager.license_data['premium_license']}\n"
                         f"Può usare: {license_manager.can_use_app()}")
            
            if license_manager.license_data['license_date']:
                status_msg += f"\nData attivazione: {license_manager.license_data['license_date'][:10]}"
            
            messagebox.showinfo("Stato Licenza", status_msg)
            
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel leggere lo stato: {str(e)}")
    
    def restore_original_data(self):
        """Ripristina manualmente i dati originali"""
        if self.test_manager.restore_license_data():
            messagebox.showinfo("Successo", "Dati originali ripristinati")
        else:
            messagebox.showerror("Errore", "Impossibile ripristinare i dati")
    
    def run(self):
        """Avvia l'applicazione"""
        self.root.mainloop()

if __name__ == "__main__":
    app = LicenseTestApp()
    app.run()