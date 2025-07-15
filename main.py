from moviepy.video.io.VideoFileClip import VideoFileClip
import math
import os

def dividir_video(input_path, duracao_parte=60):
    # Carrega o vídeo
    video = VideoFileClip(input_path)
    duracao_total = video.duration  # em segundos
    nome_base = os.path.splitext(os.path.basename(input_path))[0]
    pasta_saida = f"{nome_base}_partes"

    # Cria pasta de saída
    os.makedirs(pasta_saida, exist_ok=True)

    # Número de partes
    total_partes = math.ceil(duracao_total / duracao_parte)

    print(f"Dividindo em {total_partes} partes de até {duracao_parte} segundos...")

    for i in range(total_partes):
        inicio = i * duracao_parte
        fim = min((i + 1) * duracao_parte, duracao_total)
        subclip = video.subclip(inicio, fim)
        saida = os.path.join(pasta_saida, f"{nome_base}_parte{i+1}.mp4")
        subclip.write_videofile(saida, codec="libx264", audio_codec="aac")
    
    print("✅ Divisão concluída!")

# Exemplo de uso
dividir_video("meuvideo.mp4", duracao_parte=60)  # divide em partes de 60 segundos
