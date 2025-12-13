from pydantic import BaseModel

class CvResult(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    degree: str | None = None