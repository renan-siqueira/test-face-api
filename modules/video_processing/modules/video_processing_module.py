import os
import cv2


def extract_frames(video_path, output_dir, frame_rate, ensure_directory, use_video_fps=False, interval_in_seconds=1, use_frame_number_as_name=False):
    """Extract frames from video at a specified rate."""
    ensure_directory(output_dir)
    video_capture = cv2.VideoCapture(video_path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    
    # Valida o fps do vídeo
    if fps <= 0:
        video_capture.release()
        raise ValueError(f"O valor de FPS do vídeo '{video_path}' é inválido (fps = {fps}).")

    # Define o intervalo de frames
    if use_video_fps:
        # Calcula o intervalo com base em segundos, ignorando o frame_rate
        frame_interval = int(fps * interval_in_seconds)
    else:
        # Usa frame_rate diretamente para extrair a cada N frames
        frame_interval = max(1, frame_rate)

    frame_count = 0
    saved_frame_count = 1  # Inicializa a contagem para iniciar o nome do frame a partir de 1

    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            # Define o nome do arquivo com o número do frame no vídeo ou em sequência
            frame_number = frame_count + 1 if use_frame_number_as_name else saved_frame_count
            frame_filename = os.path.join(output_dir, f"frame_{frame_number:09d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_frame_count += 1
        frame_count += 1

    video_capture.release()


def process_videos(config, utils):
    input_videos_path = config.get("input_videos_path")
    frames_path = config.get("frames_path")
    frame_rate = config.get("frame_rate")
    use_video_fps = config.get("use_video_fps")
    interval_in_seconds = config.get("interval_in_seconds")
    use_frame_number_as_name = config.get("use_frame_number_as_name")
    allowed_extensions = config.get("allowed_extensions")

    # Verifica se os diretórios de entrada e saída existem
    if not os.path.exists(input_videos_path):
        raise FileNotFoundError(f"Diretório de entrada '{input_videos_path}' não encontrado.")
    if not os.path.exists(frames_path):
        utils['ensure_directory'](frames_path)  # Cria o diretório de saída, se não existir

    # Processa cada vídeo no diretório de entrada
    video_files = [f for f in os.listdir(input_videos_path) if any(f.endswith(ext) for ext in allowed_extensions)]
    if not video_files:
        print("Nenhum arquivo de vídeo encontrado no diretório de entrada com as extensões permitidas.")
        return

    for video_file in video_files:
        video_path = os.path.join(input_videos_path, video_file)
        output_dir = os.path.join(frames_path, os.path.splitext(video_file)[0])
        extract_frames(
            video_path, output_dir, frame_rate, utils['ensure_directory'],
            use_video_fps=use_video_fps, interval_in_seconds=interval_in_seconds,
            use_frame_number_as_name=use_frame_number_as_name
        )
