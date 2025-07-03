#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
License Manager - Sistema di gestione licenze freemium
Autore: Andrea Piani
Descrizione: Gestisce il limite di 5 utilizzi gratuiti e la licenza premium
"""

import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from datetime import datetime
import uuid

class LicenseManager:
    """Gestisce il sistema di licenze freemium"""
    
    def __init__(self):
        self.license_file = "license_data.json"
        self.max_free_uses = 5
        self.license_data = self.load_license_data()
        
    def load_license_data(self):
        """Carica i dati della licenza dal file"""
        if os.path.exists(self.license_file):
            try:
                with open(self.license_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Crea nuovi dati licenza
        return {
            'device_id': str(uuid.uuid4()),
            'uses_count': 0,
            'first_use_date': None,
            'premium_license': False,
            'license_key': None,
            'license_date': None
        }
    
    def save_license_data(self):
        """Salva i dati della licenza"""
        try:
            with open(self.license_file, 'w', encoding='utf-8') as f:
                json.dump(self.license_data, f, indent=2)
        except Exception as e:
            print(f"Errore salvando dati licenza: {e}")
    
    def increment_usage(self):
        """Incrementa il contatore degli utilizzi"""
        if not self.license_data['premium_license']:
            self.license_data['uses_count'] += 1
            if self.license_data['first_use_date'] is None:
                self.license_data['first_use_date'] = datetime.now().isoformat()
            self.save_license_data()
    
    def can_use_app(self):
        """Verifica se l'app può essere utilizzata"""
        if self.license_data['premium_license']:
            return True
        return self.license_data['uses_count'] < self.max_free_uses
    
    def get_remaining_uses(self):
        """Restituisce il numero di utilizzi rimanenti"""
        if self.license_data['premium_license']:
            return float('inf')
        return max(0, self.max_free_uses - self.license_data['uses_count'])
    
    def load_master_key(self):
        """Carica la chiave master dal file .env"""
        try:
            with open('.env', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('MASTER_LICENSE_KEY='):
                        return line.split('=', 1)[1]
        except FileNotFoundError:
            print("File .env non trovato")
        except Exception as e:
            print(f"Errore leggendo .env: {e}")
        return None
    
    def validate_license_key(self, license_key):
        """Valida una chiave di licenza contro la chiave master"""
        master_key = self.load_master_key()
        if not master_key:
            return False
        
        # Confronta direttamente con la chiave master
        return license_key.strip() == master_key.strip()
    
    def activate_premium_license(self, license_key):
        """Attiva la licenza premium"""
        if self.validate_license_key(license_key):
            self.license_data['premium_license'] = True
            self.license_data['license_key'] = license_key
            self.license_data['license_date'] = datetime.now().isoformat()
            self.save_license_data()
            return True
        return False
    
    def show_license_dialog(self, parent):
        """Mostra la finestra di acquisto licenza"""
        dialog = LicenseDialog(parent, self)
        return dialog.result

class LicenseDialog:
    """Dialog per l'acquisto della licenza premium"""
    
    def __init__(self, parent, license_manager):
        self.license_manager = license_manager
        self.result = None
        
        # Crea finestra dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Licenza Premium - Mouse Auto Clicker")
        self.dialog.geometry("600x800")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centra la finestra
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (800 // 2)
        self.dialog.geometry(f"600x800+{x}+{y}")
        
        self.setup_ui()
        
        # Aspetta che la finestra sia chiusa
        self.dialog.wait_window()
    
    def setup_ui(self):
        """Configura l'interfaccia del dialog"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titolo
        title_label = ttk.Label(main_frame, text="🚀 Sblocca Mouse Auto Clicker Premium!", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 25))
        
        # Messaggio di benvenuto
        welcome_frame = ttk.Frame(main_frame)
        welcome_frame.pack(fill=tk.X, pady=(0, 20))
        
        welcome_text = "Acquista la licenza Premium per utilizzare l'app senza limiti!"
        
        ttk.Label(welcome_frame, text=welcome_text, font=('Arial', 13), 
                 justify=tk.CENTER, wraplength=550).pack()
        
        # Caratteristiche Premium
        features_frame = ttk.LabelFrame(main_frame, text="✨ Caratteristiche Premium", padding="15")
        features_frame.pack(fill=tk.X, pady=(0, 20))
        
        features = [
            "✅ Utilizzi illimitati",
            "✅ Tutte le funzioni avanzate",
            "✅ Sequenze e macro personalizzate",
            "✅ Gestione profili completa",
            "✅ Supporto prioritario",
            "✅ Aggiornamenti gratuiti",
            "✅ Nessuna pubblicità"
        ]
        
        for feature in features:
            ttk.Label(features_frame, text=feature, font=('Arial', 12)).pack(anchor=tk.W, pady=3)
        
        # Prezzo
        price_frame = ttk.Frame(main_frame)
        price_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(price_frame, text="💰 Prezzo: €9.99 (una tantum)", 
                 font=('Arial', 16, 'bold'), foreground='green').pack()
        ttk.Label(price_frame, text="Nessun abbonamento - Paghi una volta, usi per sempre!", 
                 font=('Arial', 12)).pack(pady=(8, 0))
        
        # Informazioni acquisto
        purchase_frame = ttk.LabelFrame(main_frame, text="🛒 Come Acquistare", padding="15")
        purchase_frame.pack(fill=tk.X, pady=(0, 20))
        
        info_text = "Per acquistare la licenza Premium:\n" \
                   "1. Contatta il supporto via WhatsApp o email\n" \
                   "2. Effettua il pagamento di €9.99\n" \
                   "3. Riceverai la chiave di licenza\n" \
                   "4. Inserisci la chiave qui sotto per attivare"
        
        ttk.Label(purchase_frame, text=info_text, font=('Arial', 12), 
                 justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 15))
        
        # Pulsanti di contatto
        contact_frame = ttk.Frame(purchase_frame)
        contact_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(contact_frame, text="📱 WhatsApp (Veloce)", 
                  command=self.open_whatsapp_support).pack(fill=tk.X, pady=(0, 8))
        
        ttk.Button(contact_frame, text="📧 Email Supporto", 
                  command=self.open_email_support).pack(fill=tk.X)
        
        # Inserimento chiave licenza
        license_frame = ttk.LabelFrame(main_frame, text="🔑 Hai già una licenza?", padding="15")
        license_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(license_frame, text="Inserisci la tua chiave di licenza:", 
                 font=('Arial', 12)).pack(anchor=tk.W, pady=(0, 8))
        
        self.license_key_var = tk.StringVar()
        license_entry = ttk.Entry(license_frame, textvariable=self.license_key_var, 
                                 font=('Arial', 16, 'bold'), width=35, state='normal')
        license_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        license_entry.focus_set()  # Imposta il focus sul campo
        
        # Placeholder text
        placeholder_text = "Inserisci qui la tua chiave di licenza..."
        license_entry.insert(0, placeholder_text)
        license_entry.config(foreground='gray')
        
        def on_focus_in(event):
            if license_entry.get() == placeholder_text:
                license_entry.delete(0, tk.END)
                license_entry.config(foreground='black')
        
        def on_focus_out(event):
            if not license_entry.get():
                license_entry.insert(0, placeholder_text)
                license_entry.config(foreground='gray')
        
        license_entry.bind('<FocusIn>', on_focus_in)
        license_entry.bind('<FocusOut>', on_focus_out)
        
        activate_button = ttk.Button(license_frame, text="🔓 Attiva Licenza", 
                                    command=self.activate_license)
        activate_button.pack(pady=(0, 10))
        
        # Bind Enter key per attivare la licenza
        license_entry.bind('<Return>', lambda e: self.activate_license())
        
        # Pulsanti finali
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text="❌ Chiudi", 
                  command=self.close_dialog).pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(button_frame, text="ℹ️ Più Informazioni", 
                  command=self.open_info_page).pack(side=tk.RIGHT)
        
        # Device ID per supporto
        device_frame = ttk.Frame(main_frame)
        device_frame.pack(fill=tk.X, pady=(20, 0))
        
        device_id = self.license_manager.license_data['device_id'][:8]
        ttk.Label(device_frame, text=f"Device ID (per supporto): {device_id}...", 
                 font=('Arial', 10), foreground='gray').pack()
    
    def open_whatsapp_support(self):
        """Apre WhatsApp per contattare il supporto"""
        device_id = self.license_manager.license_data['device_id'][:8]
        message = f"Ciao! Vorrei acquistare la licenza Premium per Mouse Auto Clicker.\n\nDevice ID: {device_id}...\n\nGrazie!"
        
        # Crea link WhatsApp
        import urllib.parse
        whatsapp_url = f"https://wa.me/393516248936?text={urllib.parse.quote(message)}"
        webbrowser.open(whatsapp_url)
        
        messagebox.showinfo("WhatsApp Supporto", 
                           "Ti abbiamo aperto WhatsApp con un messaggio precompilato.\n"
                           "Invia il messaggio per ricevere assistenza immediata!")
    
    def open_email_support(self):
        """Apre email per contattare il supporto"""
        device_id = self.license_manager.license_data['device_id'][:8]
        subject = "Richiesta Licenza Premium Mouse Auto Clicker"
        body = f"Ciao,\n\nVorrei acquistare la licenza Premium per Mouse Auto Clicker.\n\nDevice ID: {device_id}...\n\nGrazie!"
        
        # Crea link mailto
        import urllib.parse
        mailto_url = f"mailto:andreapiani.dev@gmail.com?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
        webbrowser.open(mailto_url)
        
        messagebox.showinfo("Email Supporto", 
                           "Ti abbiamo aperto il client email con un messaggio precompilato.\n"
                           "Invia l'email per ricevere istruzioni per l'acquisto.")
    
    def open_info_page(self):
        """Apre la pagina informazioni"""
        webbrowser.open("https://www.andreapiani.com/autoclicker/premium")
    
    def activate_license(self):
        """Attiva la licenza inserita"""
        license_key = self.license_key_var.get().strip()
        
        # Rimuovi il placeholder se presente
        if license_key == "Inserisci qui la tua chiave di licenza...":
            license_key = ""
        
        if not license_key:
            messagebox.showerror("Errore", "Inserisci una chiave di licenza valida")
            return
        
        if self.license_manager.activate_premium_license(license_key):
            messagebox.showinfo("Successo!", 
                               "Licenza Premium attivata con successo!\n"
                               "Ora puoi utilizzare l'app senza limiti.")
            self.result = 'activated'
            self.dialog.destroy()
        else:
            messagebox.showerror("Errore", "Chiave di licenza non valida.\n\nVerifica di aver inserito correttamente la chiave ricevuta.")
    
    def close_dialog(self):
        """Chiude il dialog"""
        self.result = 'closed'
        self.dialog.destroy()

# Funzione rimossa - ora si usa solo la chiave master dal file .env

if __name__ == "__main__":
    # Test del sistema di licenze
    lm = LicenseManager()
    print(f"Device ID: {lm.license_data['device_id']}")
    print(f"Utilizzi rimanenti: {lm.get_remaining_uses()}")
    print(f"Può usare app: {lm.can_use_app()}")
    
    # Test chiave master
    master_key = lm.load_master_key()
    if master_key:
        print(f"Chiave master caricata: {master_key[:5]}...")
        print(f"Chiave valida: {lm.validate_license_key(master_key)}")
    else:
        print("Chiave master non trovata nel file .env")