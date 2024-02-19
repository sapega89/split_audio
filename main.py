import io
from typing import Annotated
from zipfile import ZipFile

from fastapi import FastAPI, UploadFile, File
from fastapi.openapi.docs import get_swagger_ui_oauth2_redirect_html, get_swagger_ui_html
from moviepy.video.io.VideoFileClip import VideoFileClip
from starlette.responses import Response, StreamingResponse, FileResponse

app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()



@app.post("/")
async def root(file: Annotated[bytes, File()], seconds: int = 30):
    with open('test.mp4', 'wb')as new_file:
        new_file.write(file)
        clip = VideoFileClip(new_file.name)
        clips = []
        with ZipFile('file.zip', 'w') as zip_object:
            iter_count = (clip.duration // seconds) + 1
            seconds_count = 0

            for count in range(int(iter_count)):
                clip = clip.subclip(0, seconds)
                seconds_count +=seconds
                file_name = f"test{count}.mp3"
                clip.audio.write_audiofile(file_name)
                zip_object.write(file_name)

    return FileResponse(path='file.zip', filename='file.zip', media_type='multipart/form-data')
