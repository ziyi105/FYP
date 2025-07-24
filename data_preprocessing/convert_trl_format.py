import json
import os

with open("C:/Users/ahziy/robocasa/robocasa/annotations.json", "r") as f:
    annotations = json.load(f)

transformed_data = []

for image_name, data in annotations.items():
    original_image = data["original_image"]
    coordinates = data["coordinates"]
    generated_files = data["generated_files"]

    if len(coordinates) != len(generated_files):
        print(f"Warning: Mismatch in lengths for {image_name}. Skipping this entry.")
        continue

    for coord, gen_file in zip(coordinates, generated_files):
        entry = {
            "scene_image_with_cross": gen_file,
            "original_scene": original_image,
            "red_cross_coordinate": coord,
            "descriptions": []
        }
        transformed_data.append(entry)

with open("C:/Users/ahziy/robocasa/robocasa/transformed_annotations.json", "w") as f:
    json.dump(transformed_data, f, indent=4)

print("Data transformation complete. Saved to 'transformed_annotations.json'.")
