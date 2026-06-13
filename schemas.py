from pydantic import BaseModel
class JobOffer(BaseModel):
    id: int
    firma: str
    stanowisko: str
    link: str
    technologie: str
    dodatkowe_info: str
    wynagrodzenie: str
    data_publikacji: str
    zrodlo: str
    priorytet: int
    class Config:
        from_attributes = True
