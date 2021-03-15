from sqlalchemy.orm import Session

from app.interfaces.api_interfaces import RepositoryInterface
from app.models import screenshot_model as model
from app.schemas import screenshot_schema as schema
from app.utils.uuid import generate_uuid


class ScreenshotRepository(RepositoryInterface):

    def reads(
            db: Session, skip: int = 0, limit: int = 100,):
        return db.query(
            model.Screenshot
        ).offset(skip).limit(limit).all()

    def read(db: Session, screenshot_id: str):
        return db.query(
            model.Screenshot
        ).filter(model.Screenshot.id == screenshot_id).first()

    def create(db: Session, screenshot: schema.ScreenshotCreate):
        uuid = generate_uuid()
        db_screenshot = model.Screenshot(
            id=uuid,
            url=screenshot.url,
            file_extension=screenshot.file_extension,
            directory=screenshot.directory,)
        db.add(db_screenshot)
        db.commit()
        db.refresh(db_screenshot)
        return db_screenshot

    def update(
                db: Session,
                screenshot: schema.ScreenshotCreate,
                screenshot_id: str
            ):
        db.query(
            model.Screenshot
        ).filter(
            model.Screenshot.id == screenshot_id
        ).update({
            model.Screenshot.url: screenshot.url,
            model.Screenshot.file_extension: screenshot.file_extension,
            model.Screenshot.directory: screenshot.directory,
        })

        db.commit()
        return db.query(
            model.Screenshot
        ).filter(model.Screenshot.id == screenshot_id).first()

    def delete(db: Session, screenshot_id: int):
        db.query(
            model.Screenshot
        ).filter(model.Screenshot.id == screenshot_id).delete()
        db.commit()
        return True
