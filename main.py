from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine
from fastapi.staticfiles import StaticFiles
from ranker import ocena_oferty
from notifer import wyslij_powiadomienie


# Importy Twoich scraperów z folderu scrapers/
from scrapers.pracuj_scraper import scrapuj_pracuj
from scrapers.justjoin_scraper import scrapuj_justjoinit
from scrapers.theprotocol_scraper import scrapuj_theprotocol

# Tworzy tabelę jeśli nie istnieje
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mój Agregator Ofert Pracy")


app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Funkcja "mózg" - pobiera oferty i wrzuca do bazy
def proces_agregacji(db: Session):
    print("Rozpoczynam cykl zbierania danych...")
    wszystkie_oferty = []
    
    # Wywołujemy po kolei Twoje skrypty
    try: wszystkie_oferty.extend(scrapuj_pracuj())
    except Exception as e: print(f"Błąd Pracuj.pl: {e}")
        
    try: wszystkie_oferty.extend(scrapuj_theprotocol())
    except Exception as e: print(f"Błąd TheProtocol: {e}")
        
    try: wszystkie_oferty.extend(scrapuj_justjoinit())
    except Exception as e: print(f"Błąd JustJoinIT: {e}")
    nowe_do_wyslania = []
    dodane = 0
    for oferta_dict in wszystkie_oferty:
        # Sprawdzamy czy link już jest w bazie (zapobiega duplikatom)
        istnieje = db.query(models.JobOffer).filter(models.JobOffer.link == oferta_dict["link"]).first()
        if not istnieje:
            nowy_wpis = models.JobOffer(**oferta_dict)
            nowy_wpis.priorytet = ocena_oferty(nowy_wpis)
            db.add(nowy_wpis)
            nowe_do_wyslania.append(nowy_wpis)
            dodane += 1
            
    db.commit()
    print(f"Agregacja zakończona. Dodano {dodane} nowych ofert.")

    if nowe_do_wyslania:
        wyslij_powiadomienie(nowe_do_wyslania)
# Endpoint do odpalenia zbierania (zrzut z przeglądarki lub CRON)
@app.post("/zbieraj/")
def uruchom_agregacje(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(proces_agregacji, db)
    return {"message": "Zaczynamy zbierać oferty w tle!"}

# Endpoint do czytania ofert (Twoje propozycje)
@app.get("/oferty/", response_model=list[schemas.JobOffer])
def pobierz_oferty(tech: str = None, db: Session = Depends(get_db)):
    query = db.query(models.JobOffer)
    if tech:
        query = query.filter(models.JobOffer.technologie.ilike(f"%{tech}%"))
    return query.order_by(models.JobOffer.id.desc()).all()
