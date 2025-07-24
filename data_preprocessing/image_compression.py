from PIL import Image
from langchain_core.messages import HumanMessage
import json
from PIL import Image

folder_path = "C:/Users/ahziy/robocasa/robocasa/cropped_images"

# for filename in os.listdir(folder_path):
#     if filename.lower().endswith((".jpeg")): 
#         image_path = os.path.join(folder_path, filename)

#         # Open the image
#         with Image.open(image_path) as img:
#             rotated_img = img.rotate(180, expand=True)
#             base, ext = os.path.splitext(image_path)
#             new_image_path = base + ".jpeg"
#             rotated_img.save(new_image_path, "JPEG")

# print("✅ All images rotated by 90 degrees successfully!")

# import os

# Folder containing images (change this to your folder path)

# Loop through all files in the folder
# for filename in os.listdir(folder_path):
#     # Check if the file is a .png file
#     if filename.lower().endswith(".png"):
#         file_path = os.path.join(folder_path, filename)
        
#         # Delete the .png file
#         os.remove(file_path)
#         print(f"Deleted: {filename}")

# print("✅ All .png files have been deleted.")

import json
import os

# Path to your JSON file
json_path = "C:/Users/ahziy/robocasa/robocasa/transformed_annotations.json"  # Replace with your actual JSON file path
output_json_path = "C:/Users/ahziy/robocasa/robocasa/transformed_annotations.json"  # Path to save the modified JSON file

# Load the JSON data
with open(json_path, "r") as f:
    data = json.load(f)

# Loop through the data and modify paths ending with .png to .jpeg
for item in data:
    # Check and modify 'scene_image_with_cross' if it ends with .png
    if item["original_scene"].lower().endswith(".png"):
        item["original_scene"] = item["original_scene"].replace(".png", ".jpeg")

    # # Check and modify 'original_scene' if it ends with .png
    # if item["original_scene"].lower().endswith(".png"):
    #     item["original_scene"] = item["original_scene"].replace(".png", ".jpeg")

# Save the modified data back to a new JSON file
with open(output_json_path, "w") as f:
    json.dump(data, f, indent=4)

print("✅ All '.png' file paths have been updated to '.jpeg'.")

