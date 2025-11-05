from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
import cv2
import requests
import os

app = FastAPI(title="Gerador de thumb de video")

OUTPUT_DIR = "thumbnails"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"messagem": "API de geração de thumbnail ativa! Use /thumbnail?url=<link_do_video>" }

@app.get("/thumbnail")
def gerar_thumbnail(
    url: str = Query(..., description="URL do vídeo (MP4, MOV, etc)"),
    tempo_segundos: int = Query(5, description="Segundo do vídeo para capturar a thumbnail")
):
    try:
        # Baixar o vídeo da URL fornecida
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code != 200:
            return JSONResponse(status_code=400, content={"error": "Não foi possível baixar o vídeo."})
        
        video_path = os.path.join(OUTPUT_DIR, "temp_video.mp4")
        with open(video_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)


        # Captura o frame
        video = cv2.VideoCapture(video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_target = int(fps * tempo_segundos)
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_target)

        sucesso, frame = video.read()

        if not sucesso:
            return JSONResponse(status_code=400, content={"erro": "Não foi possível capturar o frame."})
        
        thumbnail_path = os.path.join(OUTPUT_DIR, "thumbnail.jpg")
        cv2.imwrite(thumbnail_path, frame)

        video.release()
        os.remove(video_path) # limpa o arquivo temporário

        # Retorna a imagem gerada
        return FileResponse(thumbnail_path, media_type="image/jpeg", filename="thumbnail.jpg")
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})
