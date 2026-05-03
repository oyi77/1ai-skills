"""Authentication routes."""

from fastapi import APIRouter, Depends, HTTPException, Request

from src.api.models.auth import LoginRequest, TokenResponse, UserCreate, UserResponse
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.user_repo import UserRepository
from src.infrastructure.auth.jwt import JWTHandler
from src.infrastructure.auth.password import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

jwt_handler = JWTHandler()


async def get_user_repo(request: Request):
    async for db in get_db():
        yield UserRepository(db)


@router.post("/register", response_model=TokenResponse)
async def register(
    data: UserCreate,
    request: Request,
    repo: UserRepository = Depends(get_user_repo),
):
    existing = await repo.get_by_email(data.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    password_hash = hash_password(data.password)
    user_id = await repo.create_user(data.email, data.name, password_hash, data.role)
    user = await repo.get_by_id(user_id)

    token = jwt_handler.create_token(
        subject=user_id,
        additional_claims={
            "tenant_id": user.get("tenant_id", "default"),
            "role": user.get("role", "user"),
        },
    )

    return TokenResponse(access_token=token, token_type="bearer", user=UserResponse(**user))


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    request: Request,
    repo: UserRepository = Depends(get_user_repo),
):
    user = await repo.get_by_email(data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user.get("banned"):
        raise HTTPException(status_code=403, detail="Account is banned")
    if not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    await repo.update_last_login(user["id"])

    token = jwt_handler.create_token(
        subject=user["id"],
        additional_claims={
            "tenant_id": user.get("tenant_id", "default"),
            "role": user.get("role", "user"),
        },
    )

    return TokenResponse(access_token=token, token_type="bearer", user=UserResponse(**user))


@router.get("/me", response_model=UserResponse)
async def get_me(
    request: Request,
    repo: UserRepository = Depends(get_user_repo),
):
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(**user)
