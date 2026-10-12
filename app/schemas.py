from pydantic import BaseModel, Field


class GreetingRequest(BaseModel):
    # Keep the request body small and explicit so the example stays easy to follow.
    name: str = Field(..., min_length=1, max_length=60, examples=["Sudheer"])


class GreetingResponse(BaseModel):
    message: str
    received_name: str
    timestamp: str
