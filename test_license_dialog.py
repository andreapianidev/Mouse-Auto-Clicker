#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test per la finestra di licenza migliorata
Autore: Andrea Piani
Descrizione: Test per verificare la compatibilità Windows della finestra licenza
"""

import tkinter as tk
from license_manager import LicenseManager, LicenseDialog

def test_license_dialog():
    """Test della finestra di licenza"""
    # Crea finestra principale
    root = tk.Tk()
    root.title("Test Licenza Dialog")
    root.geometry("400x300")
    
    # Centra la finestra
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (400 // 2)
    y = (root.winfo_screenheight() // 2) - (300 // 2)
    root.geometry(f"400x300+{x}+{y}")
    
    # Crea license manager
    license_manager = LicenseManager()
    
    def open_license_dialog():
        """Apre la finestra di licenza"""
        dialog = LicenseDialog(root, license_manager)
        print(f"Risultato dialog: {dialog.result}")
    
    # Pulsante per aprire il dialog
    open_button = tk.Button(root, text="Apri Finestra Licenza", 
                           command=open_license_dialog,
                           font=('Segoe UI', 12),
                           padx=20, pady=10)
    open_button.pack(expand=True)
    
    # Info
    info_label = tk.Label(root, 
                         text="Clicca il pulsante per testare\nla finestra di licenza migliorata",
                         font=('Segoe UI', 10),
                         justify=tk.CENTER)
    info_label.pack(pady=20)
    
    # Avvia il loop
    root.mainloop()

if __name__ == "__main__":
    test_license_dialog()