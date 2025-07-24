import json
import re

def clean_text(text):
    # Normalize whitespace and punctuation, remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    # Convert full-width characters to half-width (if applicable)
    text = text.translate(str.maketrans({
        '‘': "'", '’': "'", '“': '"', '”': '"'
    }))
    text = text.lower()
    text = text.replace('.', '')
    text = text.replace('- ', '')
    text = text.replace('it is ', '')
    text = text.replace('located ', '')
    text = text.replace('stool', 'chair')
    text = text.replace('positioned', '')

    return text

def process_descriptions(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cleaned_data = {}
    for image_path, details in data.items():
        cleaned_descriptions = [clean_text(desc) for desc in details.get("descriptions", [])]
        cleaned_data[image_path] = {
            "scene_image_with_cross": details.get("scene_image_with_cross", ""),
            "original_scene": details.get("original_scene", ""),
            "red_cross_coordinate": details.get("red_cross_coordinate", []),
            "descriptions": cleaned_descriptions
        }
    
    # Save the cleaned data back to the JSON file
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=4, ensure_ascii=False)
    
    return cleaned_data

# Example usage
json_file = "C:/Users/ahziy/robocasa/robocasa/annotations.json"
cleaned_data = process_descriptions(json_file)
for image_path, details in cleaned_data.items():
    print(f"Image: {image_path}")
    print("Cleaned Descriptions:")
    for desc in details["descriptions"]:
        print(f"- {desc}")
    print("\n" + "-"*50 + "\n")
