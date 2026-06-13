import cloudscraper
from bs4 import BeautifulSoup
import time

def scrapuj_pracuj():
    print("[Pracuj.pl] Uruchamianie scrapera...")
    scrapper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )
    scrapper.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })

    bazowy_url = "https://it.pracuj.pl/praca/skawina;wp?rd=20&et=17%2C4"
    widziane_oferty = set()
    numer_strony = 1
    zebrane_oferty = []

    while True:
        print(f"[Pracuj.pl] Pobieranie strony nr {numer_strony}...")
        url = bazowy_url if numer_strony == 1 else f"{bazowy_url}&pn={numer_strony}"
        
        response = scrapper.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            oferty = soup.select('div[class^="offer-tile"]')

            if not oferty:
                print("[Pracuj.pl] Dotarto do końca wyników.")
                break

            for oferta in oferty:
                stanowisko = oferta.select_one('[data-test="link-offer-title"]')
                if not stanowisko: continue
                    
                stanowisko_text = stanowisko.text.strip()
                link_wzgledny = stanowisko.get('href')
                link_pelny = f"{link_wzgledny}" if link_wzgledny else "Brak linku"

                firma = oferta.select_one('[data-test="text-company-name"]')
                firma_text = firma.text.strip().split('\n')[0].strip() if firma else 'Brak informacji o nazwie'

                tech_container = oferta.select_one('[data-test="technologies-list"]')
                if tech_container:
                    tech_spans = tech_container.select('[data-test="technologies-item"]')
                    technologie_text = ', '.join([span.text.strip() for span in tech_spans])
                else:
                    technologie_text = 'Brak wymienionych technologii'

                info_elementy = oferta.select('[data-test^="offer-additional-info-"]')
                dodatkowe_info_text = ', '.join([info.text.strip() for info in info_elementy]) if info_elementy else 'Brak dodatkowych informacji'

                wynagrodzenie = oferta.select_one('[data-test="offer-salary"]')
                wynagrodzenie_text = wynagrodzenie.text.strip() if wynagrodzenie else 'Brak informacji o zarobkach'

                dodano = oferta.select_one('[data-test="text-added"]')
                dodano_text = dodano.text.strip() if dodano else 'Brak daty'

                if link_pelny in widziane_oferty:
                    continue
                widziane_oferty.add(link_pelny)

                # DOŁĄCZAMY SŁOWNIK DO LISTY
                zebrane_oferty.append({
                    "firma": firma_text,
                    "stanowisko": stanowisko_text,
                    "link": link_pelny,
                    "technologie": technologie_text,
                    "dodatkowe_info": dodatkowe_info_text,
                    "wynagrodzenie": wynagrodzenie_text,
                    "data_publikacji": dodano_text,
                    "zrodlo": "Pracuj.pl"
                })

            numer_strony += 1
            time.sleep(2)
        else:
            print(f'[Pracuj.pl] Błąd pobierania. Kod HTTP: {response.status_code}')
            break
            
    return zebrane_oferty
