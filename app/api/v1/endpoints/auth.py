from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, RefreshTokenRequest
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)
from app.core.config import settings

router = APIRouter()


# ✅ REGISTER
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    new_user = User(
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "usuario creado"}


# ✅ LOGIN
@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    access_token = create_access_token(data={"sub": str(db_user.id)})
    refresh_token = create_refresh_token(data={"sub": str(db_user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# ✅ REFRESH (ESTE ES EL IMPORTANTE)
@router.post("/refresh")
def refresh_token(request: RefreshTokenRequest):
    try:
        payload = jwt.decode(
            request.refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        new_access_token = create_access_token(data={"sub": user_id})

        return {
            "access_token": new_access_token
        }

    except Exception:
        raise HTTPException(status_code=401, detail="Refresh token inválido")