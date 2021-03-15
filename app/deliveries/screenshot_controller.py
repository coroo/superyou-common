from fastapi import Depends, APIRouter, HTTPException, status
# from fastapi import Depends, APIRouter, HTTPException, status, Query
from env import settings
from sqlalchemy.orm import Session
from typing import List
from app.schemas import screenshot_schema, user_schema, general_schema
from app.usecases.screenshot_service import ScreenshotService as usecase
from app.middlewares import deps, di, auth
# import asyncio
from pyppeteer import launch

router = APIRouter()
local_prefix = "/screenshot/"


class ScreenshotController():

    @router.post(local_prefix)
    async def create_screenshoot(
            screenshot: screenshot_schema.ScreenshotCreate,
            db: Session = Depends(deps.get_db),
            current_user: user_schema.User = Depends(
                auth.get_current_active_user)
            ):
        if (
                screenshot.file_extension is None or
                screenshot.file_extension == ""):
            screenshot.file_extension = 'pdf'
        res = usecase.create(db=db, screenshot=screenshot)

        # if not using docker
        # browser = await launch()
        # if using docker
        browser = await launch(
            headless=True,
            executablePath="/usr/bin/chromium-browser",
            args=['--no-sandbox', '--disable-gpu']
        )
        page = await browser.newPage()
        await page.goto(screenshot.url, {
            'waitUntil': 'networkidle2',
            'waitLoad': True,
            'waitNetworkIdle': True,
            'networkidle2': True
        })
        await page.pdf({
            'path': ''+settings.PUBLIC_URL+'/'+res.id+'.'+res.file_extension})
        await page.evaluate('''() => {
            return {
                width: document.documentElement.clientWidth,
                height: document.documentElement.clientHeight,
                deviceScaleFactor: window.devicePixelRatio,
            }
        }''')
        await browser.close()

        res.redirect_to = (
            settings.APP_URL+'/'+settings.PUBLIC_URL
            + '/'+res.id+'.'+res.file_extension)
        return res

    @router.put(local_prefix+"{screenshot_id}",
                response_model=screenshot_schema.Screenshot)
    def update_screenshot(
                screenshot_id: str,
                screenshot: screenshot_schema.ScreenshotCreate,
                db: Session = Depends(deps.get_db),
                current_user: user_schema.User = Depends(
                    auth.get_current_active_user)
            ):
        db_screenshot = usecase.read(db, screenshot_id=screenshot_id)
        if db_screenshot is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Screenshot not found")
        return usecase.update(
            db=db,
            screenshot=screenshot,
            screenshot_id=screenshot_id)

    @router.get(
        local_prefix,
        response_model=List[screenshot_schema.Screenshot])
    def read_screenshots(
            commons: dict = Depends(di.common_parameters),
            db: Session = Depends(deps.get_db),
            ):
        screenshots = usecase.reads(
                db,
                skip=commons['skip'],
                limit=commons['limit'],
            )
        return screenshots

    @router.get(local_prefix+"{screenshot_id}",
                response_model=screenshot_schema.Screenshot)
    def read_screenshot(
            screenshot_id: str,
            db: Session = Depends(deps.get_db),
            ):
        db_screenshot = usecase.read(
            db,
            screenshot_id=screenshot_id,)
        if db_screenshot is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Screenshot not found")
        return db_screenshot

    @router.delete(local_prefix, response_model=general_schema.Delete)
    def delete_screenshot(
                screenshot: screenshot_schema.ScreenshotId,
                db: Session = Depends(deps.get_db),
                current_user: user_schema.User = Depends(
                    auth.get_current_active_user)
            ):
        db_screenshot = usecase.read(db, screenshot_id=screenshot.id)
        if db_screenshot is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Screenshot not found")
        usecase.delete(db=db, screenshot_id=screenshot.id)
        return {"id": screenshot.id}
