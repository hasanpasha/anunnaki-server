from pydantic import BaseModel


class Result(BaseModel):
    success: bool
    error: str = None