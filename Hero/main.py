from typing import List
from fastapi import FastAPI, HTTPException, Query, Depends
from sqlmodel import Session, select
from config import create_db_and_tables, engine
from models import Hero, HeroCreate, HeroRead, HeroUpdate


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

def get_session():
    with Session(engine) as session:
        yield session

@app.post("/create-hero/", response_model=HeroRead)
def create_hero(*,session: Session = Depends(get_session),hero: HeroCreate):
    db_hero = Hero.from_orm(hero)
    session.add(db_hero)
    session.commit()        
    session.refresh(db_hero)
    return db_hero

@app.get("/heroes", response_model=List[HeroRead])
def list_heroes(*, session: Session=Depends(get_session),offset: int = 0, limit: int = Query(default=100, lte=100)):
    statement = select(Hero).offset(offset).limit(limit)
    heroes = session.exec(statement).all()        
    return heroes

@app.get('/heroes/{hero_id}', response_model=HeroRead)
def list_hero(*,session: Session = Depends(get_session),hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail='Hero not found')
    return hero


@app.patch("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(*,session: Session = Depends(get_session),hero_id: int, hero: HeroUpdate):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.dict(exclude_unset=True) # exclude_unset tells pydantic not to send data that wasn't set by the client

    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@app.delete('/heroes/{hero_id}')
def delete_hero(*,session: Session = Depends(get_session),hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail='Hero not found')
    session.delete(hero)
    session.commit()
    return {'ok': True}