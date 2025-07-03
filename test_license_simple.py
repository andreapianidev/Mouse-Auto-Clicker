#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test semplice per la finestra di licenza
Autore: Andrea Piani
Descrizione: Test rapido della finestra di licenza senza modificare dati esistenti
"""

import tkinter as tk
from license_manager import LicenseManager, LicenseDialog

def test_license_dialog():
    """Test rapido della finestra di licenza"""
    root = tk.Tk()
    root.withdraw()  # Nascondi la finestra principale
    
    try:
        # Crea un license manager temporaneo
        license_manager = LicenseManager()
        
        # Forza la creazione di una finestra di licenza
        # indipendentemente dallo stato attuale
        dialog = LicenseDialog(root, license_manager)
        
        print(f"Risultato dialog: {dialog.result}")
        
    except Exception as e:
        print(f"Errore durante il test: {e}")
    
    finally:
        root.destroy()

if __name__ == "__main__":
    print("Avvio test finestra di licenza...")
    test_license_dialog()
    print("Test completato.")