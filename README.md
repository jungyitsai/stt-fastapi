# STT FastAPI Server with Faster-Whisper

本專案為語音轉文字（STT, Speech-to-Text）伺服器，使用 [FastAPI](https://fastapi.tiangolo.com/) 搭配 [faster-whisper](https://github.com/guillaumekln/faster-whisper) 實作，支援 Hugging Face 與本地模型路徑自動載入，並可透過 Docker Compose 快速部署。

---

## 🚀 功能介紹

- 支援語音檔案（.wav, .mp3, .m4a 等）上傳
- 使用 faster-whisper 執行語音辨識
- 可選擇使用 Hugging Face 預設模型名稱（tiny, base, ...）
- 或直接使用放在 `/models/{model_name}` 下的本地模型
- API 錯誤清晰，支援 Swagger UI 測試
- 可一鍵啟動部署（含模型）

---

## 📁 專案結構

```
stt-fastapi/
├── app/
│   ├── main.py               # FastAPI 主程式
│   └── whisper_handler.py    # Whisper 模型邏輯
├── models/                   # ✅ 請放置本地語音模型資料夾
│   └── my-custom-whisper/    # 可自定義名稱 ( **對應 open-webui stt 模型輸入的名稱** )
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 🧑‍💻 快速啟動

### 1. 放置模型（若使用本地模型）

將你下載好的 Whisper 模型資料夾（需包含 `model.bin`, `config.json`, 等）放入專案的 `./models/` 目錄中：

```
./models/my-custom-whisper/
```

### 2. 啟動服務

```bash
docker-compose up --build
```

啟動後伺服器位於 [http://localhost:8000](http://localhost:8000)

---

## 📫 API 使用方式

### POST `/audio/transcriptions`

#### 請求參數（`multipart/form-data`）

| 欄位名稱 | 類型        | 說明                       |
|----------|-------------|----------------------------|
| `file`   | `UploadFile`| 音訊檔案（必填）           |
| `model`  | `str`       | 模型名稱（預設為 `tiny`） <br>可使用 HuggingFace 模型 ID 或 `models/` 中的資料夾名稱 |

#### 回應範例

```json
{
  "text": "這是轉錄後的語音內容"
}
```

### Swagger 文件

打開瀏覽器：[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 測試範例

```bash
curl -X POST http://localhost:8000/audio/transcriptions \
  -F "file=@test.wav" \
  -F "model=my-custom-whisper"
```

---

## 📦 支援模型列表

### Hugging Face 預設模型（直接使用名稱）

- `tiny`
- `base`
- `small`
- `medium`
- `large-v1`
- `large-v2`
- `large-v3`

### 本地模型（請放置在 `/models/` 資料夾）

- `my-custom-whisper` → `/models/my-custom-whisper/`

程式會自動補上 `/models/` 路徑，無需手動指定。

---

## 📌 錯誤處理範例

- 若模型名稱錯誤或找不到，會回傳：

```json
{
  "detail": "模型名稱無效：'abc' 不是 HuggingFace 名稱，也不是 /models/abc 本地資料夾"
}
```

---

## 🔧 未來擴充建議

- 加入 `/available-models` API 回傳模型清單
- 支援語言強制辨識（如 zh-TW）
- 整合語音合成（TTS）成雙向語音介面
- 多任務佇列處理與轉錄進度通知

---

> Maintained by [Your Name or Team]