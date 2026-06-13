from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

def scrapuj_justjoinit():
    print("[JustJoinIT] Uruchamianie scrapera...")
    zebrane_dane = []

    with sync_playwright() as p:
        # WAŻNE na serwerach linuksowych: headless=True
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = 'https://justjoin.it/job-offers/skawina?experience-level=junior,mid&radius=20&orderBy=DESC&sortBy=published#more-filters'
        
        print("[JustJoinIT] Ładuję stronę...")
        page.goto(url)
        
        try:
            print("[JustJoinIT] Czekam na oferty...")
            page.wait_for_selector('a[href*="/job-offer/"]', timeout=30000)
        except Exception:
            print("[JustJoinIT] Brak ofert (timeout) - zła lokacja lub błąd strony.")
            browser.close()
            return zebrane_dane
        
        widziane_linki = set()
        poprzednia_ilosc = 0
        proby_bez_nowych_ofert = 0
        
        while True:
            html_strony = page.content()
            soup = BeautifulSoup(html_strony, 'html.parser')
            widoczne_oferty = soup.select('a[href*="/job-offer/"]')
            
            for oferta in widoczne_oferty:
                link_wzgledny = oferta.get('href')
                
                if link_wzgledny and link_wzgledny not in widziane_linki:
                    widziane_linki.add(link_wzgledny)
                    link_pelny = f"https://justjoin.it{link_wzgledny}"
                    
                    tytul_element = oferta.select_one('h2, h3, h4')
                    stanowisko = tytul_element.text.strip() if tytul_element else "Brak tytułu"

                    dane_tekstowe = list(oferta.stripped_strings)
                    firma = dane_tekstowe[0] if len(dane_tekstowe) > 0 else "Brak nazwy firmy"

                    zarobki = "Brak widełek"
                    for i, tekst in enumerate(dane_tekstowe):
                        if "PLN" in tekst or "EUR" in tekst or "USD" in tekst:
                            if i > 0:
                                zarobki = f"{dane_tekstowe[i-1]} {tekst}"
                            else:
                                zarobki = tekst
                            break
                            
                    # Trik dla Rankera: łączymy cały tekst z kafelka (tam są ukryte technologie!)
                    pelny_tekst_karty = ", ".join(dane_tekstowe)
                            
                    if stanowisko != "Brak tytułu":
                        zebrane_dane.append({
                            "firma": firma,
                            "stanowisko": stanowisko,
                            "link": link_pelny,
                            # Używamy małego oszustwa - UI pokaże napis, a Ranker przeczyta 'dodatkowe_info'
                            "technologie": "Szczegóły w ofercie", 
                            "dodatkowe_info": pelny_tekst_karty, 
                            "wynagrodzenie": zarobki,
                            "data_publikacji": "Brak daty",
                            "zrodlo": "JustJoinIT"
                        })
            
            obecna_ilosc = len(widziane_linki)
            
            if obecna_ilosc == poprzednia_ilosc:
                page.evaluate("window.scrollBy(0, -500)")
                time.sleep(0.5)
                page.evaluate("window.scrollBy(0, 1500)")
                time.sleep(1.5)
                
                obecna_ilosc = len(widziane_linki)
                
                if obecna_ilosc == poprzednia_ilosc:
                    proby_bez_nowych_ofert += 1
                    if proby_bez_nowych_ofert >= 3:
                        print(f"[JustJoinIT] Koniec! Przeskanowano całą stronę.")
                        break
                else:
                    proby_bez_nowych_ofert = 0
                    poprzednia_ilosc = obecna_ilosc
            else:
                proby_bez_nowych_ofert = 0
                poprzednia_ilosc = obecna_ilosc
                page.evaluate("window.scrollBy(0, 2000)")
                time.sleep(2)
                
        browser.close()
    return zebrane_dane
