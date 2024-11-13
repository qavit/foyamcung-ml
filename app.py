from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import VitsModel, AutoTokenizer
import torch
import base64
from io import BytesIO
import soundfile as sf

app = FastAPI()

# 載入 Hugging Face 模型和 tokenizer
tts_model_name = "facebook/mms-tts-hak"
tts_model = VitsModel.from_pretrained(tts_model_name)
tts_tokenizer = AutoTokenizer.from_pretrained(tts_model_name)


class TTSRequest(BaseModel):
    text: str

# 推論函式參考：
# https://huggingface.co/spaces/ninumm/mms-tts-en/blob/main/ttsFB.py
# https://huggingface.co/spaces/united-link/taiwanese-hakka-tts/blob/main/app.py


# 定義 TTS 預測 API 端點
@app.post("/predict/tts")
async def predict_tts(request: TTSRequest):
    try:
        # 將輸入文字轉換為 token
        inputs = tts_tokenizer(request.text, return_tensors="pt")

        # 模型推論
        with torch.no_grad():
            output = tts_model(**inputs).waveform

        # 取得取樣率並轉換音訊數據為 NumPy 陣列
        sampling_rate = tts_model.config.sampling_rate
        output_np = output.squeeze().cpu().numpy()

        # 將 NumPy 音訊數據轉為 WAV 格式並編碼為 Base64
        with BytesIO() as audio_bytes:
            sf.write(audio_bytes, output_np, sampling_rate, format="WAV")
            audio_bytes.seek(0)
            audio_base64 = base64.b64encode(audio_bytes.read()).decode("utf-8")

        # 返回 JSON 格式，包含取樣率和音訊 Base64 字串
        return {
            "sampling_rate": sampling_rate,
            "audio_base64": audio_base64
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
