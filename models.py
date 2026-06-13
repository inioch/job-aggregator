from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime

class JobOffer(Base):
    __tablename__ = "job_offers"

    # Główne ID w bazie
    id = Column(Integer, primary_key=True, index=True)
    
    # Dane oferty
    firma = Column(String, index=True)
    stanowisko = Column(String, index=True)
    
    # Link jest kluczowy – ustawiamy unique=True, żeby baza 
    # automatycznie odrzucała duplikaty (ten sam link nie wejdzie drugi raz)
    link = Column(String, unique=True, index=True)
    
    technologie = Column(String)       # Przechowujemy jako tekst "Python, Java, ..."
    dodatkowe_info = Column(String)    # Poziom, tryb pracy, miasto
    wynagrodzenie = Column(String)
    
    # Metadane
    data_publikacji = Column(String)   # Data z portalu
    zrodlo = Column(String, index=True) # "Pracuj.pl", "JustJoinIT", "TheProtocol"
    priorytet = Column(Integer, default=0)
    
    # Kiedy oferta została dodana do Twojej bazy (ułatwia sortowanie "najnowszych")
    fetched_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<JobOffer(stanowisko='{self.stanowisko}', firma='{self.firma}')>"
