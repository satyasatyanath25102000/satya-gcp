from datetime import datetime
from datetime import timedelta
from datetime import timezone

from jose import JWTError
from jose import jwt

from pwdlib import PasswordHash

from .config import get_app_secrets


# ==========================================
# Load application secrets
# ==========================================

secrets = get_app_secrets()

JWT_SECRET = secrets["JWT_SECRET"]

JWT_ALGORITHM = secrets.get(
    "JWT_ALGORITHM",
    "HS256",
)


ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ==========================================
# Password hashing
# ==========================================

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:

    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:

    return password_hash.verify(
        plain_password,
        hashed_password,
    )


# ==========================================
# JWT creation
# ==========================================

def create_access_token(
    user_id: str,
) -> str:

    now = datetime.now(timezone.utc)

    expire = (
        now
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": user_id,
        "iat": now,
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )

    return token


# ==========================================
# JWT verification
# ==========================================

def decode_access_token(
    token: str,
) -> str:

    payload = jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[JWT_ALGORITHM],
    )

    user_id = payload.get("sub")

    if not user_id:

        raise JWTError(
            "Missing user ID"
        )

    return user_id
