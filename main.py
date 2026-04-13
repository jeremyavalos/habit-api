from utils.security import verify_password
from utils.security import hash_password
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, Base, SessionLocal
from models.user import User
from schemas.user import UserCreate  # 👈 AQUÍ

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "API funcionando"}

@app.post("/register")
@app.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        return {"error": "usuario no encontrado"}

    if not verify_password(user.password, db_user.password):
        return {"error": "contraseña incorrecta"}

    return {"message": "login exitoso"}
    
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "usuario creado"}
