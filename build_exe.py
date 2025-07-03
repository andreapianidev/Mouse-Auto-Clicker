#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per compilare Mouse Clicker in un file .exe
Utilizzo: python build_exe.py
"""

import os
import sys
import subprocess
import shutil

def check_pyinstaller():
    """Verifica se pyinstaller è installato"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Installa pyinstaller"""
    print("Installazione di pyinstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ pyinstaller installato con successo")
        return True
    except subprocess.CalledProcessError:
        print("❌ Errore nell'installazione di pyinstaller")
        return False

def build_exe():
    """Compila l'applicazione in .exe"""
    print("Compilazione dell'applicazione...")
    
    # Comando pyinstaller
    cmd = [
        "pyinstaller",
        "--onefile",           # Un singolo file .exe
        "--windowed",          # Nasconde la console
        "--name=MouseAutoClicker", # Nome del file .exe
        "--clean",             # Pulisce cache precedenti
        "mouse_clicker.py"     # File sorgente
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Compilazione completata con successo!")
        
        # Verifica se il file è stato creato
        exe_path = os.path.join("dist", "MouseAutoClicker.exe")
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"📁 File creato: {exe_path} ({size_mb:.1f} MB)")
            
            # Copia README nella cartella dist
            if os.path.exists("README.md"):
                shutil.copy2("README.md", "dist/")
                print("📄 README.md copiato in dist/")
                
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Errore durante la compilazione: {e}")
        return False

def cleanup():
    """Pulisce i file temporanei"""
    dirs_to_remove = ["build", "__pycache__"]
    files_to_remove = ["MouseAutoClicker.spec"]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🗑️  Rimossa cartella: {dir_name}")
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"🗑️  Rimosso file: {file_name}")

def main():
    """Funzione principale"""
    print("🚀 Mouse Auto Clicker - Build Script")
    print("=" * 40)
    
    # Verifica se siamo nella directory corretta
    if not os.path.exists("mouse_clicker.py"):
        print("❌ Errore: mouse_clicker.py non trovato nella directory corrente")
        print("   Assicurati di eseguire questo script dalla cartella del progetto")
        return False
    
    # Verifica/installa pyinstaller
    if not check_pyinstaller():
        print("⚠️  pyinstaller non trovato")
        if input("Vuoi installarlo ora? (s/n): ").lower().startswith('s'):
            if not install_pyinstaller():
                return False
        else:
            print("❌ pyinstaller è necessario per la compilazione")
            return False
    else:
        print("✅ pyinstaller trovato")
    
    # Compila l'applicazione
    if build_exe():
        print("\n🎉 Compilazione completata!")
        print("\n📋 Prossimi passi:")
        print("   1. Vai nella cartella 'dist/'")
        print("   2. Troverai MouseAutoClicker.exe")
        print("   3. Puoi distribuire questo file senza Python installato")
        
        # Chiedi se pulire i file temporanei
        if input("\nVuoi pulire i file temporanei? (s/n): ").lower().startswith('s'):
            cleanup()
            print("✅ Pulizia completata")
        
        return True
    else:
        print("❌ Compilazione fallita")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ Processo completato con successo!")
        else:
            print("\n❌ Processo fallito")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Processo interrotto dall'utente")
    except Exception as e:
        print(f"\n❌ Errore inaspettato: {e}")
        sys.exit(1)