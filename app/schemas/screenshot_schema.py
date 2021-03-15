from typing import Optional
from pydantic import BaseModel


class ScreenshotBase(BaseModel):
    url: str
    directory: Optional[str] = None
    file_extension: Optional[str] = None


class ScreenshotId(BaseModel):
    id: int


class ScreenshotCreate(ScreenshotBase):
    pass


class Screenshot(ScreenshotBase):
    id: int
    redirect_to: Optional[str] = None

    class Config:
        orm_mode = True
