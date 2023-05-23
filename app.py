from fastapi import FastAPI, HTTPException
from enum import Enum
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI()

ridici: Dict = {}

vozidla: Dict = {}

class Opravneni(Enum):
    C = "C"
    CE = "C+E"
    
class Ridic(BaseModel):
    jmeno: str
    prijmeni: str
    opravneni: Opravneni
    ADR: Optional[bool] = False
    
class Uprav_ridice(BaseModel):
    jmeno: Optional[str] = None
    prijmeni: Optional[str] = None
    opravneni: Optional[Opravneni] = None
    ADR: Optional[bool] = False

class Druh_vozidla(Enum):
    solo = "solo"
    tahac = "tahač"
    naves = "návěs"
    
class Vozidlo(BaseModel):
    druh: Druh_vozidla
    spz: str
    
class Uprav_vozidlo(BaseModel):
    druh: Optional[Druh_vozidla]
    spz: Optional[str]
    
@app.get("/ridici/najdi-ridice")
async def najdi_ridice_podle_prijmeni(prijmeni: str):
    for ridic_id in ridici:
        if ridici[ridic_id].prijmeni == prijmeni:
            return ridici[ridic_id]
    raise HTTPException(status_code=404, detail="Řidič nenalezen.")

@app.get("/ridici/{ridic_id}")
async def najdi_ridice_podle_id(ridic_id: int):
    if ridic_id in ridici:
        return ridici[ridic_id]
    raise HTTPException(status_code=404, detail="Řidič nenalezen.")

@app.post("/ridici/novy-ridic/{ridic_id}")
async def novy_ridic(ridic_id: int, ridic: Ridic):
    if ridic_id in ridici:
        raise HTTPException(status_code=400, detail="Řidič již existuje.")
    ridici[ridic_id] = ridic
    return ridici[ridic_id]

@app.put("/ridici/uprav-ridice/{ridic_id}")
async def uprav_ridice(ridic_id: int, ridic: Uprav_ridice):
    if ridic_id not in ridici:
        raise HTTPException(status_code=404, detail="Řidič nenalezen.")
    if ridic.jmeno != None:
        ridici[ridic_id].jmeno = ridic.jmeno
    if ridic.prijmeni != None:
        ridici[ridic_id].prijmeni = ridic.prijmeni
    if ridic.opravneni != None:
        ridici[ridic_id].opravneni = ridic.opravneni
    if ridic.ADR != None:
        ridici[ridic_id].ADR = ridic.ADR
    return ridici[ridic_id]

@app.delete("/ridici/odstran-ridice/{ridic_id}")
async def odstran_ridice(ridic_id: int):
    if ridic_id not in ridici:
        raise HTTPException(status_code=404, detail="Řidič nenalezen.")
    del ridici[ridic_id]
    return {"Úspěch": "Řidič byl vymazán."}

@app.get("/vozidla/najdi-vozidlo")
async def najdi_vozidlo_podle_spz(spz: str):
    for vozidlo_id in vozidla:
        if vozidla[vozidlo_id].spz == spz:
            return vozidla[vozidlo_id]
    raise HTTPException(status_code=404, detail="Vozidlo nenalezeno.")

@app.get("/vozidla/{vozidlo_id}")
async def najdi_vozidlo_podle_id(vozidlo_id: int):
    if vozidlo_id in vozidla:
        return vozidla[vozidlo_id]
    return HTTPException(status_code=404, detail="Vozidlo nenalezeno.")

@app.post("/vozidla/nove-vozidlo")
async def nove_vozidlo(vozidlo_id: int, vozidlo: Vozidlo):
    if vozidlo_id in vozidla:
        raise HTTPException(status_code=400, detail="Vozidlo již existuje.")
    vozidla[vozidlo_id] = vozidlo
    return vozidla[vozidlo_id]

@app.put("/vozidla/uprav-vozidlo/{vozidlo_id}")
async def uprav_vozidlo(vozidlo_id: int, vozidlo: Uprav_vozidlo):
    if vozidlo_id not in vozidla:
        raise HTTPException(status_code=404, detail="Vozidlo nenalezeno.")
    if vozidlo.druh != None:
        vozidla[vozidlo_id].druh = vozidlo.druh  
    if vozidlo.spz != None:
        vozidla[vozidlo_id].spz = vozidlo.spz
    return vozidla[vozidlo_id]

@app.delete("vozidla/odstran-vozidlo/{vozidlo_id}")
async def odstran_vozidlo(vozidlo_id: int):
    if vozidlo_id not in vozidla:
        raise HTTPException(status_code=404, detail="Vozidlo nenalezeno.")
    del vozidla[vozidlo_id]
    return {"Úspěch": "Vozidlo bylo vymazáno."}