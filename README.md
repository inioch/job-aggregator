cat << 'EOF' > ~/Desktop/job_aggregator_backup/README.md

# 🚀 Smart Job Aggregator & Ranker

W pełni zautomatyzowany system ETL (Extract, Transform, Load) do pozyskiwania, oceniania i monitorowania ofert pracy z polskiego rynku IT.

Zamiast ręcznego przeglądania setek ogłoszeń, aplikacja cyklicznie pobiera oferty z popularnych portali (Pracuj.pl, TheProtocol, JustJoinIT), przepuszcza je przez autorski silnik oceniający (Scoring Engine) i dostarcza tylko te najlepiej dopasowane prosto na skrzynkę e-mail oraz do responsywnego panelu webowego.

---

## ✨ Główne funkcjonalności

- **🕵️‍♂️ Zautomatyzowany Web Scraping:** Ekstrakcja danych (stanowisko, firma, wynagrodzenie, lokalizacja, technologie) z uwzględnieniem paginacji stron.
- **🧠 Custom Scoring Engine (0-100 pkt):** Algorytm oceniający oferty w locie. Premiuje określony stack technologiczny oraz pracę zdalną, a bezwzględnie odrzuca technologie zdefiniowane w "czarnej liście" oraz niepłatne staże.
- **📧 System Alertów:** Automatyczne powiadomienia e-mail (via SMTP) z zestawieniem ofert, które przekroczyły zdefiniowany próg punktowy (np. > 75/100).
- **📊 Minimalistyczny Dashboard Webowy:** Front-end zbudowany w oparciu o Vanilla JS i Tailwind CSS, umożliwiający błyskawiczne filtrowanie i przeglądanie "topowych" ofert bez przeładowywania strony.
- **⚙️ Wdrożenie "Zero-Touch":** Aplikacja działa bezobsługowo w tle jako usługa systemowa Linuxa (`systemd`), a cykle agregacji wyzwalane są przez harmonogram `cron`.

---

## 🛠️ Architektura i Stack Technologiczny

Projekt został podzielony na niezależne moduły, co ułatwia jego skalowanie i ewentualne dodawanie nowych scraperów w przyszłości.

- **Backend / API:** Python, FastAPI, Uvicorn
- **Baza Danych:** SQLite, SQLAlchemy (ORM), Pydantic (Walidacja)
- **Ekstrakcja Danych:** BeautifulSoup4, Requests, Playwright
- **Frontend:** HTML5, JavaScript (Fetch API), Tailwind CSS
- **Infrastruktura:** Linux, Systemd, Cron

---

## 🚀 Uruchomienie lokalne (Development)

### Wymagania wstępne

- Python 3.10+
- Git

### Instalacja krok po kroku

**1. Sklonuj repozytorium:**
`bash
git clone https://github.com/[Twój_GitHub]/job_aggregator.git
cd job_aggregator
`

**2. Utwórz i aktywuj środowisko wirtualne:**
`bash
python3 -m venv venv
source venv/bin/activate  # Dla Windows: venv\Scripts\activate
`

**3. Zainstaluj wymagane zależności:**
`bash
pip install -r requirements.txt
`
_(Uwaga: jeśli instalujesz projekt od zera bez pliku requirements, użyj: `pip install fastapi uvicorn sqlalchemy requests beautifulsoup4 playwright`)_

**4. Uruchom serwer developerski:**
`bash
uvicorn main:app --reload
`
Aplikacja będzie dostępna pod adresem: `http://127.0.0.1:8000/static/index.html`

---

## ⚙️ Konfiguracja silnika oceniającego (Ranker)

Sercem systemu jest plik `ranker.py`. Możesz dostosować algorytm do własnych preferencji, modyfikując wagi i słowa kluczowe. System jest domyślnie skonfigurowany pod profil Junior/Mid Developera.

`python

# ranker.py - Fragment konfiguracji

technologie_top = ["python", "react", "javascript", "sql", "linux"]

# Odrzucanie niepożądanych technologii

złe_technologie = ["java", "c++", ".net"]

# Preferowane lokalizacje (np. praca hybrydowa w okolicach zamieszkania lub pełna zdalna)

if "skawina" in tekst or "kraków" in tekst or "remote" in tekst or "zdalna" in tekst:
score += 25
`

---

## 🔐 Konfiguracja powiadomień E-mail

Aby uruchomić automatyczne alerty e-mail:

1. Otwórz plik `notifier.py`.
2. Zaktualizuj zmienne środowiskowe (lub wstaw bezpośrednio, upewniając się, że plik nie trafi na repozytorium publiczne).
3. Wygeneruj **Hasło do aplikacji** w ustawieniach konta Google i przypisz je do skryptu.

---

## 🖥️ Wdrożenie na serwerze (Production)

Projekt jest przystosowany do działania jako daemon na serwerze Linux.

**1. Konfiguracja usługi Systemd** (`/etc/systemd/system/job_aggregator.service`):
`ini
[Unit]
Description=Job Aggregator API
After=network.target

[Service]
User=twoj_uzytkownik
WorkingDirectory=/sciezka/do/job_aggregator
ExecStart=/sciezka/do/job_aggregator/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
`

**2. Harmonogram zadań (Crontab):**
Konfiguracja wyzwalająca agregację np. o godzinie 6:00 i 14:00.
`bash
0 6,14 * * * curl -X POST http://127.0.0.1:8000/zbieraj/ >> /sciezka/do/logow/cron_log.txt 2>&1
`

---

## 👨‍💻 Autor

Inioch

Projekt open-source udostępniany na licencji MIT. Zachęcam do forkownia i dostosowywania systemu pod własne poszukiwania pracy!
EOF
