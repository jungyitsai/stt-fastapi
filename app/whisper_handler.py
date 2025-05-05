from faster_whisper import WhisperModel
import os

_model_cache = {}

def get_model(model_name: str = "tiny") -> WhisperModel:
    cache_key = model_name

    if cache_key not in _model_cache:
        valid_hf_names = {"tiny", "base", "small", "medium", "large-v1", "large-v2", "large-v3"}

        if model_name in valid_hf_names:
            model = WhisperModel(model_name, compute_type="int8")
        else:
            local_path = os.path.join("/models", model_name)  # ✅ 自動補上 /models/
            if os.path.isdir(local_path):
                print(f"[INFO] 載入本地模型：{local_path}")
                model = WhisperModel(local_path, compute_type="int8")
            else:
                raise ValueError(
                    f"模型名稱無效：'{model_name}' 不是 HuggingFace 名稱，也不是 /models/{model_name} 本地資料夾"
                )

        _model_cache[cache_key] = model

    return _model_cache[cache_key]

def transcribe_audio(file_path: str, model_name: str = "tiny") -> str:
    model = get_model(model_name)
    segments, _ = model.transcribe(file_path)
    return "".join(segment.text for segment in segments)
