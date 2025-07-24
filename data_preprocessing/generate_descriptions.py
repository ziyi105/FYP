import json
import openai
import base64
import os

openai.api_key = "your-api-key"

annotations_path = "C:/Users/ahziy/robocasa/robocasa/annotations.json"
output_json_path = annotations_path

with open(annotations_path, "r") as f:
    annotations = json.load(f)

scene_groups = [
    [f"C:/Users/ahziy/robocasa/robocasa/annotated_images\\cropped_scene_{i}.jpeg" for i in range(1, 9)],
    [f"C:/Users/ahziy/robocasa/robocasa/annotated_images\\cropped_scene_{i}.jpeg" for i in range(9, 18)],
    [f"C:/Users/ahziy/robocasa/robocasa/annotated_images\\cropped_scene_{i}.jpeg" for i in range(18, 26)],
    [f"C:/Users/ahziy/robocasa/robocasa/annotated_images\\cropped_scene_{i}.jpeg" for i in range(26, 34)],
    [f"C:/Users/ahziy/robocasa/robocasa/annotated_images\\cropped_scene_{i}.jpeg" for i in range(34, 43)],
    [f"C:/Users/ahziy/robocasa/robocasa/annotated_images\\cropped_scene_{i}.jpeg" for i in range(43, 51)],
    [f"C:/Users/ahziy/robocasa/robocasa/annotated_images\\cropped_scene_{i}.jpeg" for i in range(51, 59)],
    [f"C:/Users/ahziy/robocasa/robocasa/annotated_images\\cropped_scene_{i}.jpeg" for i in range(59, 67)],
    [f"C:/Users/ahziy/robocasa/robocasa/annotated_images\\cropped_scene_{i}.jpeg" for i in range(67, 75)],
    [f"C:/Users/ahziy/robocasa/robocasa/annotated_images\\cropped_scene_{i}.jpeg" for i in range(75, 83)],
    [f"C:/Users/ahziy/robocasa/robocasa/annotated_images\\cropped_scene_{i}.jpeg" for i in range(83, 91)],
    [f"C:/Users/ahziy/robocasa/robocasa/annotated_images\\cropped_scene_{i}.jpeg" for i in range(91, 100)],
    [f"C:/Users/ahziy/robocasa/robocasa/annotated_images\\cropped_scene_{i}.jpeg" for i in range(100, 108)],
    [f"C:/Users/ahziy/robocasa/robocasa/annotated_images\\cropped_scene_{i}.jpeg" for i in range(108, 116)],
    [f"C:/Users/ahziy/robocasa/robocasa/annotated_images\\cropped_scene_{i}.jpeg" for i in range(116, 124)],
    [f"C:/Users/ahziy/robocasa/robocasa/annotated_images\\cropped_scene_{i}.jpeg" for i in range(124, 132)],
    [f"C:/Users/ahziy/robocasa/robocasa/annotated_images\\cropped_scene_{i}.jpeg" for i in range(132, 140)],
    [f"C:/Users/ahziy/robocasa/robocasa/annotated_images\\cropped_scene_{i}.jpeg" for i in range(140, 148)]
]
scene_groups_length = [8, 9, 8, 8, 9, 8, 8, 8, 8, 8, 8, 9, 8, 8, 8, 8, 8, 8]
cross_labels = ["cross_1", "cross_2", "cross_3", "cross_4"]

def generate_descriptions(reference_image_path):
    """Generates descriptions for all 4 cross positions based on the reference image."""
    descriptions_per_cross = {}

    for i in range(1, 5):
        cross_image_path = reference_image_path.replace(".jpeg", f"_cross_{i}.jpeg")

        if not os.path.exists(cross_image_path):
            print(f"Skipping {cross_image_path}: File not found.")
            continue

        print(f"Generating descriptions for: {cross_image_path}")

        with open(cross_image_path, "rb") as image_file:
            image_path = base64.b64encode(image_file.read()).decode("utf-8")

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "The scene image shows a kitchen with a red cross. Generate exactly four distinct and specific descriptions of its position using nearby fixed objects (e.g., refrigerator, countertop, stove) as reference points. Do not use the words 'red cross'. Output only the four descriptions, with each one immediately following the previous on a new line, without extra blank lines, numbers, dashes, or any other text."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_path}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "Describe the position of the cross."
                        }
                    ]
                }
            ],
            response_format={"type": "text"},
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        generated_descriptions = response["choices"][0]["message"]["content"].strip().split("\n")
        accepted_descriptions = []

        for desc in generated_descriptions:
            print(f"Generated: {desc}")
            while True:
                user_input = input("Accept description? (Y/n/edit/add): ").strip().lower()
                if user_input == "edit":
                    desc = input("Enter your description: ").strip()
                elif user_input == "n":
                    break
                elif user_input == "add":
                    new_desc = input("Enter additional description: ").strip()
                    accepted_descriptions.append(new_desc)
                    continue  
                else: 
                    accepted_descriptions.append(desc)
                    break

        descriptions_per_cross[f"cross_{i}"] = accepted_descriptions

    return descriptions_per_cross

resume_group = 14
start_index = sum(scene_groups_length[:resume_group]) 

for group_idx in range(resume_group, len(scene_groups)):
    scene_group = scene_groups[group_idx]
    length_of_image_group = scene_groups_length[group_idx]  
    end_index = start_index + length_of_image_group
    reference_image = scene_group[0]
    print(f"Generating descriptions based on reference image: {reference_image}")

    cross_label_descriptions = generate_descriptions(reference_image)  

    for img_idx, scene_image in enumerate(scene_group):
        for cross_label in cross_label_descriptions.keys():
            scene_cross_image = scene_image.replace(".jpeg", f"_{cross_label}.jpeg")
            if scene_cross_image in annotations:
                annotations[scene_cross_image]["descriptions"] = cross_label_descriptions[cross_label]
    start_index = end_index  

    with open(output_json_path, "w") as f:
        json.dump(annotations, f, indent=4)
    print(f"Annotations updated and written after processing group {group_idx + 1}")

print(f"Test JSON saved at: {output_json_path}")
