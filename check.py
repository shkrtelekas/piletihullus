from playwright.sync_api import sync_playwright
import urllib.request
import json
import os

def loe_lehed(failinimi="lehed.txt"):
    lehed = []
    with open(failinimi, "r") as f:
        for rida in f:
            rida = rida.strip()
            if rida and not rida.startswith("#"):
                nimi = rida.split("/performances/")[-1].split("?")[0]
                nimi = nimi.split("-", 1)[-1].replace("-", " ").title()
                lehed.append({"nimi": nimi, "url": rida})
    return lehed

def on_pilet_saadaval(page, url):
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(3000)
    nupp = page.query_selector("a.btn.btn-default.pull-right")
    lehe_algus = page.content()[:200]
    print(f"  Lehe algus: {lehe_algus}")
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
    lehed = loe_lehed()
    print(f"Kontrollin {len(lehed)} etendust...")

    leitud = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for leht in lehed:
            print(f"Kontrollin: {leht['nimi']}...")
            if on_pilet_saadaval(page, leht["url"]):
                print(f"  ✅ PILETID SAADAVAL: {leht['nimi']}")
                leitud.append((leht["nimi"], leht["url"]))
            else:
                print(f"  ❌ Pole saadaval")
        browser.close()

    if leitud:
        saada_teade(leitud)
        print("Teavitus saadetud!")

if __name__ == "__main__":
    main()
