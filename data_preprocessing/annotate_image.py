import os
import cv2
import numpy as np
import json

click_positions = []
grid_size = (14, 14)  
annotations = {}  

def draw_grid(img, grid_size):
    """Draws a reference grid on the image."""
    height, width = img.shape[:2]
    cell_width, cell_height = width // grid_size[1], height // grid_size[0]
    
    grid_img = img.copy()
    for i in range(1, grid_size[0]):
        cv2.line(grid_img, (0, i * cell_height), (width, i * cell_height), (0, 255, 0), 1)
    for j in range(1, grid_size[1]):
        cv2.line(grid_img, (j * cell_width, 0), (j * cell_width, height), (0, 255, 0), 1)

    return grid_img, cell_width, cell_height

def click_event(event, x, y, flags, param):
    """Handles mouse click events to capture grid coordinates."""
    global click_positions, img, cell_width, cell_height

    if event == cv2.EVENT_LBUTTONDOWN:
        row, col = y // cell_height, x // cell_width 
        click_positions.append((row, col))

        cv2.line(img, (x - 10, y - 10), (x + 10, y + 10), (0, 0, 255), 2)
        cv2.line(img, (x - 10, y + 10), (x + 10, y - 10), (0, 0, 255), 2)

        cv2.imshow("Click to place 4 crosses", img)

        if len(click_positions) == 4:
            cv2.destroyAllWindows()

def annotate_image(original_img, coordinates, output_paths):
    """Generates 4 separate annotated images, each with one cross."""
    height, width = original_img.shape[:2]
    cell_width, cell_height = width // grid_size[1], height // grid_size[0]

    for i, (row, col) in enumerate(coordinates):
        annotated_img = original_img.copy()

        x, y = col * cell_width + cell_width // 2, row * cell_height + cell_height // 2

        cv2.line(annotated_img, (x - 10, y - 10), (x + 10, y + 10), (0, 0, 255), 2)
        cv2.line(annotated_img, (x - 10, y + 10), (x + 10, y - 10), (0, 0, 255), 2)

        cv2.imwrite(output_paths[i], annotated_img)

def save_annotations(json_path):
    """Saves the annotation data to a JSON file."""
    with open(json_path, "w") as f:
        json.dump(annotations, f, indent=4)
    print(f"\nAnnotations saved to {json_path}")

def process_images(image_groups, input_folder, output_folder, json_path):
    os.makedirs(output_folder, exist_ok=True)

    for group_index, group in enumerate(image_groups):
        print(f"\nProcessing group {group_index + 1} with {len(group)} images.")

        reference_image = group[0]
        img_path = os.path.join(input_folder, reference_image)

        global img, cell_width, cell_height, click_positions
        click_positions = []

        img = cv2.imread(img_path)

        if img is None:
            print(f"Could not open {img_path}. Skipping.")
            continue

        img, cell_width, cell_height = draw_grid(img, grid_size)
        cv2.imshow("Click to place 4 crosses", img)
        cv2.setMouseCallback("Click to place 4 crosses", click_event)
        cv2.waitKey(0)

        if len(click_positions) != 4:
            print(f"Skipping group {group_index + 1} because 4 points were not selected.")
            continue

        for img_file in group:
            img_path = os.path.join(input_folder, img_file)
            original_img = cv2.imread(img_path)

            if original_img is None:
                print(f"Could not open {img_path}. Skipping.")
                continue

            base_name = os.path.splitext(img_file)[0]

            output_paths = [
                os.path.join(output_folder, f"{base_name}_cross_{i+1}.png") for i in range(4)
            ]

            annotations[img_file] = {
                "original_image": img_file,
                "coordinates": click_positions,
                "generated_files": output_paths
            }

            annotate_image(original_img, click_positions, output_paths)

            print(f"Annotated images saved: {', '.join(output_paths)}")

    save_annotations(json_path)

input_folder = "C:/Users/ahziy/robocasa/robocasa/cropped_images"
output_folder = "C:/Users/ahziy/robocasa/robocasa/annotated_images"
json_path = "C:/Users/ahziy/robocasa/robocasa/annotations.json"

image_groups = [
    [f"cropped_scene_{i}.png" for i in range(1, 9)],
    [f"cropped_scene_{i}.png" for i in range(9, 18)],
    [f"cropped_scene_{i}.png" for i in range(18, 26)],
    [f"cropped_scene_{i}.png" for i in range(26, 34)],
    [f"cropped_scene_{i}.png" for i in range(34, 43)],
    [f"cropped_scene_{i}.png" for i in range(43, 51)],
    [f"cropped_scene_{i}.png" for i in range(51, 59)],
    [f"cropped_scene_{i}.png" for i in range(59, 67)],
    [f"cropped_scene_{i}.png" for i in range(67, 75)],
    [f"cropped_scene_{i}.png" for i in range(75, 83)],
    [f"cropped_scene_{i}.png" for i in range(83, 91)],
    [f"cropped_scene_{i}.png" for i in range(91, 100)],
    [f"cropped_scene_{i}.png" for i in range(100, 108)],
    [f"cropped_scene_{i}.png" for i in range(108, 116)],
    [f"cropped_scene_{i}.png" for i in range(116, 124)],
    [f"cropped_scene_{i}.png" for i in range(124, 132)],
    [f"cropped_scene_{i}.png" for i in range(132, 140)],
    [f"cropped_scene_{i}.png" for i in range(140, 148)]
]

process_images(image_groups, input_folder, output_folder, json_path)
