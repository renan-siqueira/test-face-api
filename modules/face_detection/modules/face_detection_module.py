import os
import json
import time
from datetime import datetime
import cv2
import face_recognition
from huggingface_hub import hf_hub_download
from ultralytics import YOLO
from supervision import Detections
from PIL import Image

def detect_faces_yolo(frame, model_path=None):
    """Detecta rostos usando o modelo YOLOv8."""
    if model_path is None:
        # Baixa o modelo YOLOv8 da Hugging Face se o caminho do modelo não for fornecido
        model_path = hf_hub_download(repo_id="arnabdhar/YOLOv8-Face-Detection", filename="model.pt")
    
    model = YOLO(model_path)
    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    output = model(pil_image)
    detections = Detections.from_ultralytics(output[0])
    
    face_locations = []
    for box in detections.xyxy:
        top, left, bottom, right = int(box[1]), int(box[0]), int(box[3]), int(box[2])
        face_locations.append({"top": top, "right": right, "bottom": bottom, "left": left})
    return face_locations, "yolov8-fine"  # Retorna também o tipo do modelo

def detect_faces_local(frame, detection_parameters):
    """Detecta rostos usando o modelo local com parâmetros especificados."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    model = detection_parameters.get("model", "hog")
    upscale_factor = detection_parameters.get("number_of_times_to_upsample", 1)
    face_locations = face_recognition.face_locations(rgb_frame, number_of_times_to_upsample=upscale_factor, model=model)
    return [{"top": loc[0], "right": loc[1], "bottom": loc[2], "left": loc[3]} for loc in face_locations], model

def detect_faces_api(frame, api_service, api_credentials):
    """Placeholder para a detecção usando API externa."""
    return [{"top": 50, "right": 100, "bottom": 150, "left": 75}], "api"  # Retorna também o tipo do modelo

def process_frame(frame, config):
    """Processa um frame para detectar rostos conforme o método especificado."""
    local_detection = config.get("local_detection", {})
    yolo_detection = config.get("yolo_detection", {})
    api_detection = config.get("api_detection", {})
    
    if yolo_detection.get("use_yolo"):
        model_path = yolo_detection.get("yolo_model_path")
        return detect_faces_yolo(frame, model_path)
    elif local_detection.get("use_local"):
        return detect_faces_local(frame, local_detection)
    elif api_detection.get("use_api"):
        api_service = api_detection.get("api_service")
        api_credentials = None
        api_credentials_path = api_detection.get("api_credentials_path")
        if api_credentials_path:
            with open(api_credentials_path, 'r', encoding='utf-8') as f:
                api_credentials = json.load(f)
        return detect_faces_api(frame, api_service, api_credentials)
    else:
        raise ValueError("Nenhum método de detecção foi ativado.")

def process_all_frames(config, utils):
    frames_path = config.get("frames_path")
    faces_output_path = config.get("faces_output_path")
    create_model_folder = config.get("create_model_folder", False)
    
    # Define o nome da pasta de saída com base no método e no modelo
    if create_model_folder:
        if config["yolo_detection"].get("use_yolo"):
            model_name = "yolov8-fine"
        elif config["local_detection"].get("use_local"):
            model_name = config["local_detection"].get("model", "default_model")
        elif config["api_detection"].get("use_api"):
            model_name = "api"
        else:
            model_name = "default"

        faces_output_path = os.path.join(faces_output_path, model_name)
    
    utils['ensure_directory'](faces_output_path)

    for root, dirs, files in os.walk(frames_path):
        for frame_file in files:
            if frame_file.endswith('.jpg'):
                frame_path = os.path.join(root, frame_file)
                frame = cv2.imread(frame_path)
                
                # Início da medição do tempo de processamento
                start_time = time.time()

                # Processa o frame e obtém as detecções junto com o tipo de modelo
                face_locations, model_type = process_frame(frame, config)
                
                # Fim da medição do tempo de processamento
                processing_time = time.time() - start_time

                # Calcula metadados do frame
                height, width = frame.shape[:2]
                frame_number = int(os.path.splitext(frame_file)[0].split('_')[-1])

                # Estrutura enriquecida para o resultado de saída
                detection_result = {
                    "frame_file": frame_file,
                    "timestamp": datetime.now().isoformat(),
                    "detection_method": model_type,
                    "num_faces_detected": len(face_locations),
                    "face_locations": face_locations,
                    "frame_metadata": {
                        "width": width,
                        "height": height,
                        "frame_number": frame_number
                    },
                    "processing_time_seconds": round(processing_time, 4),
                    "api_details": {
                        "service": config["api_detection"].get("api_service") if model_type == "api" else "not_applicable",
                        "status": "success" if model_type == "api" else "not_applicable",
                        "response_time": "0.25s" if model_type == "api" else "not_applicable"
                    }
                }

                relative_path = os.path.relpath(root, frames_path)
                output_subdir = os.path.join(faces_output_path, relative_path)
                utils['ensure_directory'](output_subdir)

                output_file = os.path.join(output_subdir, f"{os.path.splitext(frame_file)[0]}_faces.json")
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(detection_result, f, indent=4)
