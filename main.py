from fastapi import FastAPI, UploadFile, status, Request
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse
#import whisper
import os
from datetime import timedelta

#dotenv.load_dotenv()


app = FastAPI()
"""
def transcribe_video(filename):
    #transcribe the given video data and return the transcript
    model = whisper.load_model("base")
    transcript = model.transcribe(filename)
    segments = transcript['segments']
    srtFilename = filename.split('.')[0]+'.srt'
    try:
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            for segment in segments:
                startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
                endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
                text = segment['text']
                segmentId = segment['id']+1
                segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
                srtFile.write(segment)
        return srtFilename
    except:
        return JSONResponse({"message": "Video not found"}, status_code=404)
"""
def iterfile(path):
        try:
            with open(path, mode="rb") as file_like:
                yield from file_like
        except FileNotFoundError:
            return JSONResponse({"message": "Video not found"}, status_code=404)

@app.post("/upload_video", status_code=status.HTTP_201_CREATED)
async def save_video(video: UploadFile):
    "saves video to database"
    try:
        file_name = video.filename
        with open(file_name, "wb") as buffer:
            buffer.write(await video.read())
        return {"message": "Video uploaded successfully",
                "filename": file_name}
    except Exception as e:
        return JSONResponse({"message": "Video not found"}, status_code=404)

@app.get("/get_video/{path}", status_code=status.HTTP_200_OK)
async def get_video(path: str):
    "gets video from database"
    try:
        if os.path.exists(path):
            return StreamingResponse(iterfile(path), media_type="video/mp4")
        else:
            return JSONResponse({"message": "Video not found"}, status_code=404)
    except:
        return JSONResponse({"message": "Video not found"}, status_code=404)

"""
@app.get("/get_transcript/{path}", status_code=status.HTTP_200_OK)
async def get_transcript(path: str):
    "gets transcript from database"
    try:
        if os.path.exists(path):
            transcript = transcribe_video(path)
            return FileResponse(transcript, media_type="application/x-subrip")
        else:
            return JSONResponse({"message": "Video not found"}, status_code=404)
    except:
        return JSONResponse({"message": "Video not found"}, status_code=404)
"""