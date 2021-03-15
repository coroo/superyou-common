from sqlalchemy.orm import Session

from app.interfaces.api_interfaces import ServiceInterface
from app.repositories.screenshot_repository import (
    ScreenshotRepository as repository)
from app.schemas import screenshot_schema as schema


class ScreenshotService(ServiceInterface):
    def reads(db: Session, skip: int = 0, limit: int = 100,):
        res = repository.reads(
            db, skip=skip, limit=limit)
        return res

    def read(
            db: Session,
            screenshot_id: str,):
        res = repository.read(
            db,
            screenshot_id=screenshot_id)
        return res

    def create(db: Session, screenshot: schema.ScreenshotCreate):
        return repository.create(db=db, screenshot=screenshot)

    def update(
                db: Session,
                screenshot: schema.ScreenshotCreate,
                screenshot_id: str
            ):
        return repository.update(
            db=db,
            screenshot=screenshot,
            screenshot_id=screenshot_id)

    def delete(db: Session, screenshot_id: str):
        return repository.delete(db=db, screenshot_id=screenshot_id)
