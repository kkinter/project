from auth.auth import decode_jwt
from database.database import SessionLocal
from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Create a database session
db = SessionLocal()

# Create an API router
router = APIRouter()

# Define the OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# Utility function to get user from token
async def get_user_from_token(token: str):
    user_from_token = decode_jwt(token)
    if not user_from_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )
    return user_from_token
