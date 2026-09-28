from fastapi import FastAPI, UploadFile, File

app=FastAPI()

@app.post("/upload")
async def uploadFile(file:UploadFile=File(...)):
    content_bytes= await file.read()
    content_text=content_bytes.decode("utf-8")

    return {
    "filename": file.filename,
    "content": content_text
    }
