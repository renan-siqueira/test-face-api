import os
import json
import csv
from collections import defaultdict

def run_report_generation(params, utils_functions):
    """Orchestrates the report generation process."""
    utils_functions['ensure_directory'](params["reports_output_path"])

    # Generate the reports
    generate_reports(
        association_results_path=params["association_results_path"],
        reports_output_path=params["reports_output_path"],
        csv_filename=params["csv_filename"],
        json_filename=params["json_filename"]
    )

def generate_reports(association_results_path, reports_output_path, csv_filename, json_filename):
    associations = []
    
    # Load all associations from associations.json
    associations_file = os.path.join(association_results_path, "associations.json")
    if os.path.exists(associations_file):
        with open(associations_file, 'r', encoding='utf-8') as f:
            associations = json.load(f)
    else:
        print(f"Associations file not found: {associations_file}")
        return

    # Generate enhanced JSON report with a summary header
    generate_json_report(associations, reports_output_path, json_filename)

    # Generate CSV report
    generate_csv_report(associations, reports_output_path, csv_filename)

def generate_json_report(associations, reports_output_path, json_filename):
    json_path = os.path.join(reports_output_path, json_filename)
    
    # Initialize counters and tracking structures for summary
    recognized_people = set()
    unrecognized_count = 0
    person_detection_counts = defaultdict(int)
    
    # Process each association
    for association in associations:
        person_name = association["matched_person"]
        
        if person_name == "unknown":
            unrecognized_count += 1
        else:
            recognized_people.add(person_name)
            person_detection_counts[person_name] += 1

    # Build summary header
    summary = {
        "total_detections": len(associations),
        "total_recognized_people": len(recognized_people),
        "total_unrecognized_faces": unrecognized_count,
        "recognized_people_list": list(recognized_people),
        "detection_counts_per_person": person_detection_counts
    }
    
    # Combine summary and detailed association data
    report_data = {
        "summary": summary,
        "detailed_associations": associations
    }

    # Save the enriched JSON report
    with open(json_path, mode='w', encoding='utf-8') as json_file:
        json.dump(report_data, json_file, indent=4)
    print(f"JSON report saved to {json_path}")

def generate_csv_report(associations, reports_output_path, csv_filename):
    csv_path = os.path.join(reports_output_path, csv_filename)
    with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = [
            "timestamp",
            "frame_file",
            "person_name",
            "detection_method",
            "top",
            "right",
            "bottom",
            "left",
            "absolute_image_path",
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for association in associations:
            # Desempacota a localização da face para colunas individuais
            face_location = association["face_location"]
            writer.writerow({
                "timestamp": association["timestamp"],
                "frame_file": association["frame_file"],
                "person_name": association["matched_person"],
                "detection_method": association["detection_method"],
                "top": face_location["top"],
                "right": face_location["right"],
                "bottom": face_location["bottom"],
                "left": face_location["left"],
                "absolute_image_path": association["absolute_image_path"]
            })
    print(f"CSV report saved to {csv_path}")
