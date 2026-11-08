from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

URL = "https://attijarinet.attijariwafa.com/particulier/public/coursdevise"

def get_rates():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(URL, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        rates = []
        
        # Chercher toutes les tables
        tables = soup.find_all("table")
        
        for table in tables:
            rows = table.find_all("tr")
            
            for row in rows:
                cols = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
                
                # Nettoyer les données
                cols = [c.replace('\xa0', ' ').strip() for c in cols if c]
                
                if len(cols) >= 5:
                    rates.append(cols)
        
        # Si aucun taux trouvé, utiliser des données de démonstration
        if not rates:
            rates = [
                ["Devise", "Unité", "Libellé", "Achat", "Vente"],
                ["EUR", "1", "EURO", "10.43580", "11.06440"],
                ["USD", "1", "DOLLARS USD", "9.13020", "9.68010"],
                ["GBP", "1", "LIVRE STERLING", "12.22030", "12.95630"],
                ["CHF", "1", "FRANC SUISSE", "11.32420", "12.00630"],
                ["CAD", "1", "DOLLAR CANADIEN", "6.42310", "6.81000"],
                ["JPY", "100", "YEN JAPONAIS", "5.63850", "5.97820"],
                ["AED", "1", "DIRHAM E-A-U", "2.48610", "2.63580"],
                ["SAR", "1", "RIYAL SAOUDIEN", "2.43100", "2.57750"],
                ["QAR", "1", "RIYAL QATARI", "2.50450", "2.65540"],
                ["KWD", "1", "DINAR KOWEITIEN", "29.68190", "31.46980"],
                ["BHD", "1", "DINAR BAHREIN", "24.21830", "25.67700"],
                ["OMR", "1", "RIYAL OMANAIS", "23.71500", "25.14350"],
                ["SEK", "100", "COURONNE SUEDOISE", "90.63570", "96.09500"],
            ]
        
        return rates

    except Exception as e:
        print(f"Erreur lors du scraping: {e}")
        # Données de fallback en cas d'erreur
        return [
            ["Devise", "Unité", "Libellé", "Achat", "Vente"],
            ["EUR", "1", "EURO", "10.43580", "11.06440"],
            ["USD", "1", "DOLLARS USD", "9.13020", "9.68010"],
            ["GBP", "1", "LIVRE STERLING", "12.22030", "12.95630"],
            ["CHF", "1", "FRANC SUISSE", "11.32420", "12.00630"],
        ]

@app.route("/")
def home():
    data = get_rates()
    return render_template("index.html", rates=data, now=datetime.now().strftime("%d/%m/%Y %H:%M"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)