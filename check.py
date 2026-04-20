import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

LEHED = [
    {
        "nimi": "Rahamaa",
        "url": "https://www.piletimaailm.com/performances/135039-rahamaa?lang=et_EE"
    },
    {
        "nimi": "B-koondis",
        "url": "https://www.piletimaailm.com/performances/130852-b-koondis?lang=et_EE"
    },
    {
        "nimi": "500 aastat sõprust",
        "url": "https://www.piletimaailm.com/performances/149249-500-aastat-soprust?lang=et_EE"
    },
]

def on_pilet_saadaval(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")
    # Otsime täpselt seda nuppu
    nupp = soup.find("a", class_=lambda c: c and "btn-default" in c and "pull-right" in c)
    return nupp is not None

def saada_email(leidude_nimekiri):
    saatja = "sinuemail@gmail.com"
    saaja = "sinuemail@gmail.com"
    parool = os.environ["EMAIL_PASS"]  # GitHub Secret

    sisu = "Piletid on saadaval järgmistele etendustele:\n\n"
    for nimi, url in leidude_nimekiri:
        sisu += f"  • {nimi}: {url}\n"

    msg = MIMEText(sisu)
    msg["Subject"] = "🎭 Piletid saadaval!"
    msg["From"] = saatja
    msg["To"] = saaja

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(saatja, parool)
        server.send_message(msg)

def main():
    leitud = []
    for leht in LEHED:
        print(f"Kontrollin: {leht['nimi']}...")
        if on_pilet_saadaval(leht["url"]):
            print(f"  ✅ PILETID SAADAVAL: {leht['nimi']}")
            leitud.append((leht["nimi"], leht["url"]))
        else:
            print(f"  ❌ Pole saadaval")

    if leitud:
        saada_email(leitud)
        print("Teavitus saadetud!")

if __name__ == "__main__":
    main()
