
# Report Generation Module

## Overview
This module generates structured reports from face detection and association results. The reports are generated in two formats:
1. **CSV Report** - Provides detailed information about each detected face and its association.
2. **JSON Report** - Contains a summary of the processing results and detailed information for each detection.

## Directory Structure
The expected directory structure for running this module:
```
project_root/
├── modules/
│   └── report_generation_module.py
├── settings/
│   └── config.py
├── utils/
│   └── utils.py
└── main.py
```

## Configuration
### config.py
The following configuration parameters must be set in `config.py`:
- `APP_PATH_ASSOCIATION_RESULTS`: Path to the directory containing `associations.json`.
- `APP_PATH_REPORTS_OUTPUT`: Directory where the CSV and JSON reports will be saved.
- `APP_REPORT_CSV_FILENAME`: Name of the CSV report file (default: `detection_report.csv`).
- `APP_REPORT_JSON_FILENAME`: Name of the JSON report file (default: `detection_report.json`).

## Usage
### Running the Module
The main script orchestrates the report generation process. You can specify the configuration via a JSON file or use `config.py` settings.

```bash
python main.py --json-path path/to/config.json
```

### Expected Outputs
1. **CSV Report**: A CSV file containing the following columns:
   - `timestamp`: Timestamp of the detection.
   - `frame_file`: Name of the frame file.
   - `person_name`: Name of the detected person or "unknown" if not recognized.
   - `detection_method`: Detection method used.
   - `top`, `right`, `bottom`, `left`: Coordinates of the face bounding box.
   - `absolute_image_path`: Absolute path to the image file.

2. **JSON Report**: A JSON file with:
   - `summary`: Header section with aggregate data including total detections, recognized people, and unrecognized faces.
   - `detailed_associations`: List of detailed detection entries with data similar to the CSV report.

## Example Output
### CSV
```
timestamp,frame_file,person_name,detection_method,top,right,bottom,left,absolute_image_path
2024-11-10T18:51:02.597424,frame_000000001.jpg,John Doe,yolov8-fine,116,1477,349,1284,C:/path/to/image.jpg
```

### JSON
```json
{
  "summary": {
    "total_detections": 100,
    "total_recognized_people": 5,
    "total_unrecognized_faces": 20,
    "recognized_people_list": ["John Doe", "Jane Smith"],
    "detection_counts_per_person": {"John Doe": 15, "Jane Smith": 10}
  },
  "detailed_associations": [
    {
      "timestamp": "2024-11-10T18:51:02.597424",
      "frame_file": "frame_000000001.jpg",
      "person_name": "John Doe",
      "detection_method": "yolov8-fine",
      "face_location": {"top": 116, "right": 1477, "bottom": 349, "left": 1284},
      "absolute_image_path": "C:/path/to/image.jpg"
    }
  ]
}
```

## Dependencies
- `os`
- `json`
- `csv`
- `collections`

## Notes
This module is designed for straightforward generation of reports based on face association results. For more advanced analysis or validation processes, consider implementing additional functionalities in separate modules.

## Future Improvements
For auditing and validation of detections, consider creating a new module dedicated to generating evidence files, such as visual overlays on images, for manual verification.

## License
This project is licensed under the MIT License.
