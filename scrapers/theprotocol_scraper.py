import cloudscraper
from bs4 import BeautifulSoup
import json
import time

def scrapuj_theprotocol():
    print("[TheProtocol] Uruchamianie scrapera...")
    scrapper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )
    scrapper.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })

    bazowy_url = 'https://theprotocol.it/filtry/junior,mid;p/krakow;wp'
    widziane_oferty = set()
    numer_strony = 1
    zebrane_oferty = []

    while True:
        print(f"[TheProtocol] Pobieranie strony... {numer_strony}")
        url = bazowy_url if numer_strony == 1 else f"{bazowy_url}?pageNumber={numer_strony}"
        
        response = scrapper.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find('script', id='__NEXT_DATA__')
            if not script_tag: break
                
            try:
                dane_json = json.loads(script_tag.string)
            except Exception:
                break
            
            is_supported = dane_json.get("props", {}).get("pageProps", {}).get("isSupportedBrowser", True)
            if not is_supported:
                print("[TheProtocol] Blokada Cloudflare!")
                break

            oferty = dane_json.get("props", {}).get("pageProps", {}).get("offersResponse", {}).get("offers", [])
            if not oferty: break
                
            nowe_oferty_licznik = 0
            for oferta in oferty:
                url_name = oferta.get("offerUrlName")
                if url_name:
                    pelny_link = f"https://theprotocol.it/szczegoly/praca/{url_name}"
                    
                    if pelny_link not in widziane_oferty:
                        firma = oferta.get("employer", "Brak nazwy")
                        stanowisko = oferta.get("title", "Brak tytułu")
                        
                        tech_lista = oferta.get("technologies", [])
                        technologie = ", ".join(tech_lista) if tech_lista else "Brak wymienionych technologii"
                        
                        poziomy = [p.get("value", "") for p in oferta.get("positionLevels", [])]
                        tryby = oferta.get("workModes", [])
                        miasta = {w.get("city") for w in oferta.get("workplace", []) if w.get("city")}
                        
                        elementy_info = [str(i).capitalize() for i in poziomy + tryby + list(miasta) if i]
                        dodatkowe_info = ", ".join(elementy_info) if elementy_info else "Brak dodatkowych informacji"
                        
                        wynagrodzenie = "Brak widełek"
                        salary_data = oferta.get("salary")
                        if salary_data and isinstance(salary_data, dict):
                            kwota_od = salary_data.get("from", "")
                            kwota_do = salary_data.get("to", "")
                            waluta = salary_data.get("currency", "") or salary_data.get("currencySymbol", "")
                            okres = salary_data.get("timeUnit", {}).get("shortForm", "")
                            
                            if kwota_od and kwota_do:
                                wynagrodzenie = f"{kwota_od} - {kwota_do} {waluta} / {okres}"
                            elif kwota_do:
                                wynagrodzenie = f"do {kwota_do} {waluta} / {okres}"
                        
                        data_surowa = oferta.get("publicationDateUtc", "")
                        data_publikacji = data_surowa.split("T")[0] if data_surowa else "Brak daty"
                        
                        zebrane_oferty.append({
                            "firma": firma,
                            "stanowisko": stanowisko,
                            "link": pelny_link,
                            "technologie": technologie,
                            "dodatkowe_info": dodatkowe_info,
                            "wynagrodzenie": wynagrodzenie,
                            "data_publikacji": data_publikacji,
                            "zrodlo": "TheProtocol"
                        })
                        
                        widziane_oferty.add(pelny_link)
                        nowe_oferty_licznik += 1
            
            if nowe_oferty_licznik == 0 and numer_strony > 1:
                break

            numer_strony += 1
            time.sleep(2)
        else:
            break
            
    return zebrane_oferty
