# Guida al Sistema di Licenze Freemium

## 📋 Panoramica

Questo progetto implementa un sistema di licenze **freemium** che permette:
- ✅ **5 utilizzi gratuiti** per tutti gli utenti
- ✅ **Licenza Premium illimitata** a pagamento (€9.99)
- ✅ **Codice completamente open source**
- ✅ **Compatibile con licenze open source**

## 🔧 Come Funziona

### 1. Tracking degli Utilizzi
- Il file `license_manager.py` traccia gli utilizzi in `license_data.json`
- Ogni avvio dell'app incrementa il contatore
- Dopo 5 utilizzi, viene mostrato il dialog di acquisto

### 2. Sistema di Licenze
- **Device ID unico**: Generato automaticamente per ogni installazione
- **Chiavi di licenza**: Formato `AUTOCLICKER-XXXX-XXXX-XXXX`
- **Validazione locale**: Controllo hash MD5 semplificato

### 3. Dialog di Acquisto
- Interfaccia user-friendly per l'acquisto
- Link a PayPal e Stripe per i pagamenti
- Campo per inserire chiavi di licenza esistenti

## 💰 Modello di Business

### Prezzo Consigliato
- **€9.99** (pagamento una tantum)
- Nessun abbonamento
- Licenza a vita

### Piattaforme di Pagamento
- **PayPal**: Facile integrazione, commissioni ~3.4%
- **Stripe**: Professionale, commissioni ~2.9%
- **Gumroad**: Ideale per software, commissioni ~3.5%

## 🌐 Setup del Sistema di Vendita

### 1. Crea una Landing Page
```html
<!-- Esempio: https://www.andreapiani.com/autoclicker/premium -->
<h1>Mouse Auto Clicker Premium</h1>
<p>Sblocca utilizzi illimitati per soli €9.99!</p>
<button onclick="buyWithPayPal()">Acquista con PayPal</button>
<button onclick="buyWithStripe()">Acquista con Stripe</button>
```

### 2. Integra i Pagamenti

#### PayPal
```javascript
function buyWithPayPal() {
    // Reindirizza a PayPal con parametri prodotto
    const deviceId = getUrlParameter('device_id');
    window.location.href = `https://paypal.me/tuoaccount/9.99EUR?device_id=${deviceId}`;
}
```

#### Stripe
```javascript
function buyWithStripe() {
    // Usa Stripe Checkout
    stripe.redirectToCheckout({
        lineItems: [{
            price: 'price_premium_license', // ID prezzo Stripe
            quantity: 1,
        }],
        mode: 'payment',
        successUrl: 'https://tuosito.com/success?device_id=' + deviceId,
        cancelUrl: 'https://tuosito.com/cancel',
    });
}
```

### 3. Genera Chiavi di Licenza

#### Script Server-Side (PHP/Python/Node.js)
```python
# Esempio in Python
def generate_license_key(device_id):
    import hashlib
    hash_value = hashlib.md5((device_id + "PREMIUM_LICENSE").encode()).hexdigest()[:12]
    return f"AUTOCLICKER-{hash_value[:4].upper()}-{hash_value[4:8].upper()}-{hash_value[8:12].upper()}"

# Dopo il pagamento
def on_payment_success(device_id, payment_id):
    license_key = generate_license_key(device_id)
    send_email_with_license(customer_email, license_key)
    log_sale(device_id, payment_id, license_key)
```

### 4. Email Automatiche
```python
def send_email_with_license(email, license_key):
    subject = "La tua licenza Mouse Auto Clicker Premium"
    body = f"""
    Grazie per aver acquistato Mouse Auto Clicker Premium!
    
    La tua chiave di licenza è: {license_key}
    
    Per attivarla:
    1. Apri Mouse Auto Clicker
    2. Clicca su "💎 Acquista Premium"
    3. Inserisci la chiave nel campo "Hai già una licenza?"
    4. Clicca "🔓 Attiva Licenza"
    
    Grazie per il supporto!
    """
    send_email(email, subject, body)
```

## 🔒 Sicurezza e Anti-Pirateria

### Livello Base (Attuale)
- ✅ Validazione hash MD5 locale
- ✅ Device ID unico
- ✅ Formato chiave strutturato

### Livello Avanzato (Opzionale)
```python
# Validazione server-side
def validate_license_online(license_key, device_id):
    response = requests.post('https://tuoserver.com/validate', {
        'license_key': license_key,
        'device_id': device_id,
        'app_version': '1.0.0'
    })
    return response.json()['valid']

# Crittografia RSA
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

def generate_secure_license(device_id):
    # Genera chiave con firma RSA
    private_key = load_private_key()
    message = f"{device_id}:PREMIUM:{datetime.now().isoformat()}"
    signature = private_key.sign(message.encode(), padding.PKCS1v15(), hashes.SHA256())
    return base64.b64encode(signature).decode()
```

## 📊 Analytics e Tracking

### Metriche Importanti
```python
# Traccia conversioni
def track_metrics():
    total_downloads = count_unique_device_ids()
    trial_completions = count_users_with_5_uses()
    premium_purchases = count_premium_licenses()
    
    conversion_rate = premium_purchases / trial_completions * 100
    
    print(f"Tasso di conversione: {conversion_rate:.2f}%")
```

### Dashboard Vendite
- **Google Analytics**: Traccia visite alla landing page
- **Stripe Dashboard**: Monitora pagamenti e ricavi
- **Database personalizzato**: Traccia utilizzi e conversioni

## 🚀 Strategia di Lancio

### Fase 1: Soft Launch
1. Rilascia la versione con limite di 5 utilizzi
2. Monitora feedback utenti
3. Ottimizza il processo di acquisto

### Fase 2: Marketing
1. **GitHub**: Mantieni il repository pubblico
2. **Social Media**: Condividi su Reddit, Twitter, LinkedIn
3. **Blog Post**: Scrivi articoli su come hai implementato il sistema
4. **YouTube**: Crea video tutorial

### Fase 3: Ottimizzazione
1. **A/B Test**: Testa prezzi diversi (€7.99 vs €9.99 vs €12.99)
2. **Feedback**: Raccogli recensioni e migliora il prodotto
3. **Funzionalità Premium**: Aggiungi features esclusive

## 💡 Idee per Funzionalità Premium

### Già Implementate
- ✅ Utilizzi illimitati
- ✅ Tutte le funzioni avanzate
- ✅ Gestione profili
- ✅ Sequenze e macro

### Possibili Aggiunte
- 🔄 **Sincronizzazione cloud** dei profili
- 📊 **Statistiche avanzate** di utilizzo
- 🎨 **Temi personalizzati** dell'interfaccia
- 🔧 **Hotkey globali** per controllo rapido
- 📱 **App mobile companion**
- 🤖 **Automazioni avanzate** (OCR, image recognition)
- 📈 **Export dati** in CSV/Excel
- 🔔 **Notifiche push** per promemoria

## 📝 Aspetti Legali

### Licenza Open Source
```
MIT License con Clausola Commerciale

Permesso di:
- ✅ Uso personale
- ✅ Modifica del codice
- ✅ Distribuzione
- ✅ Uso commerciale (con limitazioni)

Limitazioni:
- ❌ Rimozione del sistema di licenze
- ❌ Distribuzione di versioni "craccate"
- ❌ Uso del marchio senza permesso
```

### Privacy Policy
- Specifica quali dati raccogli (Device ID, utilizzi)
- Spiega come usi i dati (solo per licenze)
- Garantisci che non condividi dati con terzi

### Terms of Service
- Definisci i termini di utilizzo
- Specifica la politica di rimborso
- Includi disclaimer di responsabilità

## 🎯 Obiettivi di Revenue

### Scenario Conservativo
- 1000 download/mese
- 50% completa i 5 utilizzi = 500 utenti
- 5% converte a premium = 25 vendite
- Revenue mensile: 25 × €9.99 = **€249.75**
- Revenue annuale: **€2,997**

### Scenario Ottimistico
- 5000 download/mese
- 60% completa i 5 utilizzi = 3000 utenti
- 10% converte a premium = 300 vendite
- Revenue mensile: 300 × €9.99 = **€2,997**
- Revenue annuale: **€35,964**

## 🔧 Manutenzione e Supporto

### Sistema di Supporto
1. **FAQ** sulla landing page
2. **Email support**: support@tuodominio.com
3. **GitHub Issues** per bug tecnici
4. **Discord/Telegram** per community

### Aggiornamenti
- **Patch di sicurezza**: Gratuiti per tutti
- **Nuove funzionalità**: Solo per utenti Premium
- **Bug fixes**: Gratuiti per tutti

## 📞 Contatti e Supporto

Per domande sull'implementazione:
- 📧 Email: andrea@tuodominio.com
- 💬 GitHub: Apri un issue
- 🌐 Website: https://www.andreapiani.com

---

**Nota**: Questo sistema è completamente compatibile con licenze open source e permette di monetizzare il software mantenendo la trasparenza del codice.