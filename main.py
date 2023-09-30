from fastapi import FastAPI, UploadFile, status, Response
import cloudinary
import cloudinary.api
from cloudinary.uploader import upload
import dotenv
from os import getenv

dotenv.load_dotenv()

cloudinary.config(
    cloud_name=getenv("CLOUD_NAME"),
    api_key=getenv("API_KEY"),
    api_secret=getenv("API_SECRET"),
    secure=True,
)


app = FastAPI()


@app.post("/upload_video", status_code=status.HTTP_201_CREATED)
async def save_video(uthman: UploadFile):
    "saves video to database"
    file_name = uthman.filename
    content = await uthman.read()
    res = upload(content, resource_type = "video", public_id = file_name)
    return {
            "message": "Video uploaded successfully",
            "url": res["url"]
            }

@app.get("/get_video/{path}", status_code=status.HTTP_303_SEE_OTHER)
async def get_video(path: str):
    "gets video from database"
    res = cloudinary.api.resources(resource_type = "video")
    if res:
        for item in res["resources"]:
            if item["public_id"] == path:
                response = Response()
                response.status_code = status.HTTP_303_SEE_OTHER
                response.headers["Location"] = item["url"]
                return response
    else:
        
        return {"message": "Video not found"}