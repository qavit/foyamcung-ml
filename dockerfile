# 使用官方 Python 基礎映像檔
FROM python:3.9-slim

# 設置工作目錄
WORKDIR /app

# 複製所需文件
COPY . /app

# 安裝依賴
RUN pip install -r requirements.txt

# 暴露應用程式的連接埠
EXPOSE 8000

# 啟動 FastAPI 應用程式
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]