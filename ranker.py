def ocena_oferty(oferta):
    score = 0
    tekst = f"{oferta.stanowisko} {oferta.technologie} {oferta.dodatkowe_info}".lower()
    
    # --- 1. Twoje Technologie (Główny atut) ---
   
    technologie_top = [
        "python", "react", "javascript", "sql", "linux", "html", "css",
        "typescript", "node", "postgresql", "postgres"
        ]
# Dodajemy 15 punktów za KAŻDĄ technologię, którą znasz
    trafione_tech = sum(1 for tech in technologie_top if tech in tekst)
    score += (trafione_tech * 15)
    
    # --- 2. Lokalizacja i Zdalna ---
    if "skawina" in tekst or "kraków" in tekst or "remote" in tekst or "zdalna" in tekst:
        score += 25
        
    # --- 3. Rodzaj Umowy ---
    if "uop" in tekst or "umowa o pracę" in tekst:
        score += 15
        
    # --- 4. Czerwone Flagi (Odrzut) ---
    złe_technologie = ["java", " c ", "c++", "c#", ".net"]

    tekst_do_flag = tekst.replace("javascript", "js")

    if any(bad in tekst_do_flag for bad in złe_technologie):
        score -= 100  # Natychmiastowe ubicie oceny
        
    if "staż" in tekst and "płatny" not in tekst:
        score -= 100

    # Zwracamy wynik ograniczony do przedziału 0 - 100
    return max(0, min(100, score))
