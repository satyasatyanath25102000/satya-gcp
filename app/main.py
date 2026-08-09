from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException

from fastapi.security import (
    OAuth2PasswordRequestForm,
)

from sqlalchemy.orm import Session

from .auth import (
    create_access_token,
    hash_password,
    verify_password,
)

from .database import (
    Base,
    engine,
    get_db,
)

from .dependencies import (
    get_current_user,
)

from .models import User

from .schemas import (
    Token,
    UserCreate,
    UserResponse,
)


# ==========================================
# FastAPI
# ==========================================

app = FastAPI(
    title="JWT Authentication API",
    version="1.0.0",
)


# ==========================================
# Create tables
# ==========================================

Base.metadata.create_all(
    bind=engine
)


# ==========================================
# Health check
# ==========================================

@app.get("/")
def root():

    return {
        "status": "running",
        "service": "JWT Authentication API",
    }


# ==========================================
# Register
# ==========================================

@app.post(
    "/register",
    response_model=UserResponse,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):

    existing_user = (
        db.query(User)
        .filter(
            (User.username == user_data.username)
            |
            (User.email == user_data.email)
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="Username or email already exists",
        )

    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(
            user_data.password
        ),
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return UserResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        is_active=user.is_active,
    )


# ==========================================
# Login
# ==========================================

@app.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    user = (
        db.query(User)
        .filter(
            User.username
            == form_data.username
        )
        .first()
    )

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    if not verify_password(
        form_data.password,
        user.password_hash,
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    access_token = create_access_token(
        str(user.id)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# ==========================================
# Protected endpoint
# ==========================================

@app.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(
        get_current_user
    ),
):

    return UserResponse(
        id=str(current_user.id),
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
    )
