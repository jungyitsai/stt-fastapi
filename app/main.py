from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import shutil, os, traceback
from tempfile import NamedTemporaryFile
from whisper_handler import transcribe_audio

app = FastAPI()

@app.post("/audio/transcriptions")
async def transcribe_endpoint(
    file: UploadFile = File(...),
    model: str = Form("tiny")
):
    try:
        suffix = os.path.splitext(file.filename)[1]
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        text = transcribe_audio(tmp_path, model)
        return JSONResponse(content={"text": text})

    except ValueError as ve:
        # 用戶輸入錯誤，例如模型不存在
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="語音辨識失敗：" + str(e))
