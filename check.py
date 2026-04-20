import requests
from bs4 import BeautifulSoup
import urllib.request
import json
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
    {
        "nimi": "Kuningas UBU",
        "url": "https://www.piletimaailm.com/performances/145717-kuningas-ubu?lang=et_EE"
    },
]

def on_pilet_saadaval(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "et-EE,et;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
    }
    resp = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")
    nupp = soup.find("a", class_=lambda c: c and "btn-default" in c and "pull-right" in c)
    return nupp is not None

def saada_teade(leidude_nimekiri):
    token = os.environ["TG_TOKEN"]
    chat_id = os.environ["TG_CHAT_ID"]

    tekst = "🎭 Piletid saadaval!\n\n"
    for nimi, url in leidude_nimekiri:
        tekst += f"• {nimi}\n{url}\n\n"

    data = json.dumps({
        "chat_id": chat_id,
        "text": tekst
    }).encode()

    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(req)

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
        saada_teade(leitud)
        print("Teavitus saadetud!")

if __name__ == "__main__":
    main()
