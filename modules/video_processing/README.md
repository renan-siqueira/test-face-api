
# Video Processing Project

This project aims to extract frames from videos in a specified directory, allowing customization of parameters such as frame rate, use of video FPS, interval between frames, and naming of output files.

## Project Structure

The project is organized as follows:

```plaintext
video_processing/
├── main.py                        # Main file that orchestrates the video processing
├── json/
│   └── params.json                # JSON file with configuration parameters
├── settings/
│   └── config.py                  # Global project settings
├── utils/
│   └── utils.py                   # Utility functions
└── modules/
    └── video_processing_module.py # Module responsible for video processing
```

## Dependencies

- Python 3.x
- OpenCV

Install dependencies using `requirements.txt` (if required).

```bash
pip install -r requirements.txt
```

## How to Run

To run the video processing, use `main.py` and provide the path to a JSON configuration file with the required parameters.

```bash
python main.py --json-path <path_to_json_config>
```

### Example JSON Configuration File

```json
{
  "input_videos_path": "data/input_videos",
  "frames_path": "data/frames",
  "frame_rate": 5,
  "use_video_fps": false,
  "interval_in_seconds": 2,
  "use_frame_number_as_name": true,
  "allowed_extensions": [".mp4", ".avi"]
}
```

## Configuration Parameters

- `input_videos_path`: Path to the directory containing input videos.
- `frames_path`: Path to the directory where frames will be saved.
- `frame_rate`: Number of frames per second to be extracted.
- `use_video_fps`: Determines if the original video FPS will be used to calculate the interval between frames.
- `interval_in_seconds`: Interval in seconds between frames (used if `use_video_fps` is `true`).
- `use_frame_number_as_name`: Determines if frames will be named with the original frame number or in sequence.
- `allowed_extensions`: List of allowed file extensions for video files.

## Execution Example

```bash
python main.py --json-path json/params.json
```

## Code Structure

- **main.py**: Orchestrates the process and loads configurations.
- **video_processing_module.py**: Processes the video by extracting frames based on specified parameters.
- **utils.py**: Utility functions to ensure directory structure.
- **config.py**: Project configuration file, used as a fallback when JSON is not provided.

---

### Notes

Ensure the input videos are in the specified directory and that the file format matches one of the allowed extensions.
