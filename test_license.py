#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test del sistema di licenze
"""

import tkinter as tk
from license_manager import LicenseManager
import os

def test_license_system():
    """Testa il sistema di licenze"""
    print("=== Test Sistema Licenze ===")
    
    # Crea license manager
    lm = LicenseManager()
    
    print(f"Device ID: {lm.license_data['device_id'][:8]}...")
    print(f"Utilizzi attuali: {lm.license_data['uses_count']}")
    print(f"Utilizzi rimanenti: {lm.get_remaining_uses()}")
    print(f"Può usare app: {lm.can_use_app()}")
    print(f"Ha licenza premium: {lm.license_data['premium_license']}")
    
    # Test chiave master
    master_key = lm.load_master_key()
    if master_key:
        print(f"\nChiave master: {master_key}")
        print(f"Chiave valida: {lm.validate_license_key(master_key)}")
    else:
        print("\nChiave master non trovata!")
    
    # Simula utilizzi
    print("\n=== Simulazione Utilizzi ===")
    for i in range(7):
        print(f"\nUtilizzo {i+1}:")
        if lm.can_use_app():
            lm.increment_usage()
            print(f"  ✅ App utilizzata. Rimanenti: {lm.get_remaining_uses()}")
        else:
            print(f"  ❌ Limite raggiunto! Serve licenza premium.")
            break
    
    # Test attivazione licenza
    print("\n=== Test Attivazione Licenza ===")
    master_key = lm.load_master_key()
    if master_key and lm.activate_premium_license(master_key):
        print("✅ Licenza premium attivata!")
        print(f"Ora può usare app: {lm.can_use_app()}")
        print(f"Utilizzi rimanenti: {lm.get_remaining_uses()}")
    else:
        print("❌ Errore attivazione licenza o chiave master non trovata")

def test_gui():
    """Testa l'interfaccia grafica del sistema licenze"""
    root = tk.Tk()
    root.withdraw()  # Nascondi finestra principale
    
    lm = LicenseManager()
    
    # Forza il limite per testare il dialog
    lm.license_data['uses_count'] = 5
    lm.license_data['premium_license'] = False
    lm.save_license_data()
    
    print("Mostrando dialog di acquisto licenza...")
    result = lm.show_license_dialog(root)
    print(f"Risultato dialog: {result}")
    
    root.destroy()

if __name__ == "__main__":
    # Backup del file licenza esistente
    if os.path.exists("license_data.json"):
        os.rename("license_data.json", "license_data.json.backup")
    
    try:
        # Test sistema
        test_license_system()
        
        # Test GUI (opzionale)
        test_gui_input = input("\nVuoi testare l'interfaccia grafica? (y/n): ")
        if test_gui_input.lower() == 'y':
            test_gui()
        
    finally:
        # Ripristina backup
        if os.path.exists("license_data.json.backup"):
            if os.path.exists("license_data.json"):
                os.remove("license_data.json")
            os.rename("license_data.json.backup", "license_data.json")
        
    print("\n✅ Test completato!")