import re
from pytube import YouTube
import os
from shutil import copyfile
import pandas as pd
from tqdm import tqdm
import Operations

FOLDER = os.path.join("data", "videos")


def download_video(name, video_id, start_time, duration_time):

    file_path = os.path.join(FOLDER, name)
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    print(f"Descarga {name} desde YouTube: {video_id}")
    video = (
        YouTube(f"https://www.youtube.com/watch?v={video_id}")
        .streams.filter(file_extension="mp4")
        .first()
    )
    file_name = re.sub(r"[.;:,?!]", "", video.title) + ".mp4"
    if not os.path.exists(os.path.join(FOLDER, file_name)):
        video.download(FOLDER)

    output_file = os.path.join(file_path, name + "-" + video_id + ".mp4")
    if os.path.exists(output_file):
        return

    if start_time != start_time and duration_time != duration_time:
        copyfile(src=os.path.join(FOLDER, file_name), dst=output_file)
    else:
        original_video = os.path.join(FOLDER, file_name)
        try:
            os.system(
                f'ffmpeg -hide_banner -loglevel error -ss {start_time} -i "{original_video}" -to {duration_time} -c copy "{output_file}"'
            )
        except:
            print(f"Ocurrio un error al descargar {video.title}.mp4")
            #Elimina los videos utilizados para crear los clips para el dataset
            for file in os.listdir(FOLDER):
                if file.endswith(".mp4"):
                    os.remove(os.path.join(FOLDER, file))


print("\nDescarga de videos de letreros de YouTube\n")

#Crea el dataset basado en urlList.csv
df_links = pd.read_csv("data/urlList.csv")
for idx, row in tqdm(df_links.iterrows(), total=df_links.shape[0]):
    download_video(*row)

#Elimina los videos utilizados para crear los clips para el dataset
for file in os.listdir(FOLDER):
    if file.endswith(".mp4"):
        os.remove(os.path.join(FOLDER, file))


print("Creando dataset... esto puede tardar varios minutos")
#Cree un dataset de los videos donde aún no se han extraído puntos de referencia
videos = Operations.cargar_dataset()

#Crea un marco de datos de signos de referencia (nombre, modelo, distancia)
Operations.cargar_referencia_señales(videos)
print("¡Dataset gestures_dataset creado correctamente!")