import base64
import json


def save_base64_to_wav(json_path, output_wav_path):
    # 讀取 JSON 檔案
    with open(json_path, 'r') as f:
        data = json.load(f)

    # 取得 base64 字串
    audio_base64 = data['audio_base64']

    # 解碼 base64 字串
    audio_bytes = base64.b64decode(audio_base64)

    # 寫入 WAV 檔案
    with open(output_wav_path, 'wb') as f:
        f.write(audio_bytes)


if __name__ == "__main__":
    save_base64_to_wav('test_audio.json', 'test_audio.wav')
