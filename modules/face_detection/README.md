
# Face Detection Micro-Project

This micro-project provides a comprehensive solution for detecting faces in video frames using three different methods:
1. **Local Detection** (using models such as HOG or CNN from the `face_recognition` library)
2. **YOLOv8 Model** (for face detection using YOLOv8, downloaded from Hugging Face Hub)
3. **External API Detection** (via supported APIs such as Azure, Google Vision, or AWS)

Each detection method can be configured independently, and the outputs are saved in JSON format, including metadata such as detection method, processing time, and the coordinates of detected faces.

## Project Structure

The main files and directories in this project are organized as follows:

- `main.py`: The orchestrator script that loads configurations, manages parameters, and runs face detection using the specified method.
- `face_detection_module.py`: Contains the core detection logic, with functions for local, YOLO, and API-based face detection.
- `config.py`: Stores the paths and configuration settings for each detection method.
- `utils/utils.py`: Contains utility functions, including directory handling.

## Setup and Installation

1. Clone the repository to your local machine.
2. Install the dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. If you are using YOLOv8, ensure the model path is configured in `params.json` or `config.py`.

## Configuration

### Configuration File

The main configurations can be set in either a JSON configuration file (e.g., `params.json`) or in `config.py`. 
Both configuration options support the following parameters:

- **frames_path**: Path to the directory containing input frames.
- **faces_output_path**: Path to the directory where output JSON files will be saved.
- **create_model_folder**: Boolean flag to create a subfolder for the output files named after the detection method.

### Detection Method Configurations

Each detection method has its own configuration dictionary:

1. **Local Detection**: 
   - `use_local`: Boolean to enable local detection.
   - `model`: Set to either "hog" or "cnn" for face recognition.
   - `upscale_factor` and `number_of_times_to_upsample`: Parameters for controlling face detection accuracy.

2. **YOLO Detection**:
   - `use_yolo`: Boolean to enable YOLOv8 detection.
   - `yolo_model_path`: Path to the YOLOv8 model file.

3. **API Detection**:
   - `use_api`: Boolean to enable API-based detection.
   - `api_service`: Name of the API service (e.g., Azure).
   - `api_credentials_path`: Path to the API credentials file.

### Example `params.json`

```json
{
    "frames_path": "data/frames",
    "faces_output_path": "data/faces_detected",
    "create_model_folder": true,
    
    "local_detection": {
        "use_local": true,
        "model": "hog",
        "upscale_factor": 1,
        "number_of_times_to_upsample": 1
    },

    "yolo_detection": {
        "use_yolo": false,
        "yolo_model_path": "/path/to/yolo_model.pt"
    },

    "api_detection": {
        "use_api": false,
        "api_service": null,
        "api_credentials_path": null
    }
}
```

## Usage

Run the `main.py` script with the optional argument `--json-path` to specify the JSON configuration file.

```bash
python main.py --json-path path/to/params.json
```

### Example Output JSON

Each frame's output JSON includes details on:
- **Frame metadata**: Frame dimensions and sequence number.
- **Detection method**: The method used (e.g., YOLO, HOG, API).
- **Processing time**: Time taken for detection on the frame in seconds.
- **Face locations**: Coordinates of detected faces.

Example output:

```json
{
    "frame_file": "frame_000003927.jpg",
    "timestamp": "2024-11-10T14:48:55.390712",
    "detection_method": "hog",
    "num_faces_detected": 2,
    "face_locations": [
        {"top": 23, "right": 854, "bottom": 290, "left": 587},
        {"top": 162, "right": 1616, "bottom": 547, "left": 1231}
    ],
    "frame_metadata": {
        "width": 1920,
        "height": 1080,
        "frame_number": 3927
    },
    "processing_time_seconds": 0.3521,
    "api_details": {
        "service": "not_applicable",
        "status": "not_applicable",
        "response_time": "not_applicable"
    }
}
```

## Notes

- Ensure all paths and detection methods are properly configured to avoid errors.
- YOLOv8 model can be downloaded from Hugging Face if the `yolo_model_path` is not provided.

This micro-project provides flexibility to use different face detection methods based on your specific requirements. 
