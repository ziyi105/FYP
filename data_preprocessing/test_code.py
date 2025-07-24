import json

def transform_json_structure(input_file, output_file):
    """Transforms the JSON list into a dictionary where 'scene_image_with_cross' is the key."""
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Convert list into dictionary
    transformed_data = {item["scene_image_with_cross"]: item for item in data}

    # Save the transformed data back to a JSON file
    with open(input_file, "w", encoding="utf-8") as f:
        json.dump(transformed_data, f, indent=4)

# Example usage
input_json_path = "C:/Users/ahziy/robocasa/robocasa/annotations.json"
output_json_path = "path/to/your/output.json"

transform_json_structure(input_json_path, output_json_path)
print(f"Transformed JSON saved to {output_json_path}")



