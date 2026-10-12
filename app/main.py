from datetime import datetime, timezone
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import GreetingRequest, GreetingResponse


LOCAL_ORIGIN_REGEX = r"https?://(localhost|127\.0\.0\.1)(:\d+)?$"


def get_allowed_origins() -> list[str]:
    configured_origins = [
        origin.strip()
        for origin in os.getenv("FRONTEND_ORIGINS", "").split(",")
        if origin.strip()
    ]

    # Keep explicit deployed origins configurable while allowing any localhost
    # port for local React/Vite development.
    return list(dict.fromkeys(configured_origins))


app = FastAPI(
    title="Basic React FastAPI Demo",
    version="1.0.0",
    description="A tiny backend used to demonstrate a React to FastAPI flow.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_origin_regex=LOCAL_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/greet", response_model=GreetingResponse)
def greet_user(payload: GreetingRequest) -> GreetingResponse:
    cleaned_name = payload.name.strip()
    if not cleaned_name:
        raise HTTPException(status_code=422, detail="Name cannot be blank.")

    return GreetingResponse(
        message=f"Hello, {cleaned_name}! Your FastAPI backend is working.",
        received_name=cleaned_name,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
