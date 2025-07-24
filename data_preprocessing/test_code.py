# import openai
# import base64

# openai.api_key = "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"

# image_path = "C:/Users/ahziy/robocasa/robocasa/annotated_images/cropped_scene_12_cross_4.jpeg"
# with open(image_path, "rb") as image_file:
#     encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

# # print(f"Base64 image length: {len(encoded_image)} characters")

# image_data = image_path
# def generate_descriptions(image_data, coordinates):
#     """Generates descriptions using an LLM."""

#     response = openai.ChatCompletion.create(
#         model="gpt-4o",
#         messages=[
#             {
#             "role": "system",
#             "content": [
#                 {
#                 "type": "text",
#                 "text": "The scene image shows a kitchen with a red cross. Generate 8 distinct and specific descriptions for the position of the red cross. Use nearby fixtures or robot as reference. In the output, do not include any context, order of the descriptions and the word red cross. Separate each description with a new line.\n"
#                 }
#             ]
#             },
#             {
#             "role": "user",
#             "content": [
#                 {
#                 "type": "image_url",
#                 "image_url": {
#                     "url": f"data:image/jpeg;base64,{encoded_image}"
#                 }
#                 },
#                 {
#                 "type": "text",
#                 "text": "describe the position of red cross"
#                 }
#             ]
#             }
#         ],
#         response_format={
#             "type": "text"
#         },
#         temperature=1,
#         max_completion_tokens=2048,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )
#     print(response["choices"][0]["message"]["content"].strip())

# generate_descriptions(image_data, [0, 0, 0, 0])

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



