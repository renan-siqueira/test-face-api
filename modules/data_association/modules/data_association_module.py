import os
import json
import time
from datetime import datetime
import face_recognition
from tqdm import tqdm


def load_reference_faces(reference_dataset_path):
    """Load and encode faces from the reference dataset."""
    reference_encodings = {}
    for person_name in os.listdir(reference_dataset_path):
        person_path = os.path.join(reference_dataset_path, person_name)
        if os.path.isdir(person_path):
            encodings = []
            for image_file in os.listdir(person_path):
                image_path = os.path.join(person_path, image_file)
                image = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(image)
                if encoding:
                    encodings.append(encoding[0])
            reference_encodings[person_name] = encodings
    print(f"Loaded reference encodings for {len(reference_encodings)} people.")
    return reference_encodings


def associate_faces(detection_results_path, reference_encodings, similarity_threshold, utils):
    """Associate detected faces with the reference dataset based on similarity threshold."""
    associations = []
    all_files = []

    for root, _, files in os.walk(detection_results_path):
        all_files.extend([os.path.join(root, file) for file in files if file.endswith('_faces.json')])

    print("Starting face association process...")
    for file in tqdm(all_files, desc="Associating faces"):
        with open(file, 'r', encoding='utf-8') as f:
            detection_data = json.load(f)

        frame_file = detection_data["frame_file"]
        frame_path = detection_data["absolute_image_path"]
        detection_json_path = utils['format_path_for_json'](os.path.abspath(file))
        frame_metadata = detection_data["frame_metadata"]
        detection_method = detection_data["detection_method"]
        processing_time = detection_data.get("processing_time_seconds", 0)

        image = face_recognition.load_image_file(frame_path)

        face_locations = detection_data["face_locations"]
        detected_encodings = face_recognition.face_encodings(
            image, known_face_locations=[
                (loc['top'], loc['right'], loc['bottom'], loc['left']) for loc in face_locations
            ]
        )

        for idx, encoding in enumerate(detected_encodings):
            match = None
            min_distance = None
            start_time = time.time()
            
            for person, encodings in reference_encodings.items():
                distances = face_recognition.face_distance(encodings, encoding)
                best_match_index = distances.argmin()
                if distances[best_match_index] < similarity_threshold:
                    match = person
                    min_distance = distances[best_match_index]
                    break

            association_time = time.time() - start_time

            associations.append({
                "frame_file": frame_file,
                "absolute_image_path": frame_path,
                "detection_json_path": detection_json_path,
                "timestamp": datetime.now().isoformat(),
                "matched_person": match if match else "unknown",
                "similarity_distance": min_distance if min_distance else "not_matched",
                "detection_method": detection_method,
                "frame_metadata": frame_metadata,
                "face_location": face_locations[idx] if face_locations else None,
                "processing_details": {
                    "detection_time_seconds": processing_time,
                    "association_time_seconds": round(association_time, 4),
                    "method_used": "face_recognition" if match else "unknown"
                }
            })

    print("Face association process completed.")
    return associations


def save_associations(associations, output_path):
    """Save association results to a JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(associations, f, indent=4)
    print(f"Associations saved to {output_path}")


def orchestrate_data_association(params, utils):
    """Orchestrator function to manage the data association process."""
    utils['ensure_directory'](params["association_output_path"])

    reference_encodings = load_reference_faces(params["reference_dataset_path"])
    associations = associate_faces(
        params["detection_results_path"],
        reference_encodings,
        params["similarity_threshold"],
        utils
    )

    output_file = os.path.join(params["association_output_path"], "associations.json")
    save_associations(associations, output_file)
    print(f"Associations saved to {output_file}")
