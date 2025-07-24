import os
import json
import agent
from utils import grid_to_pixel_center, coordinates_to_grid_number, calculate_iou

def calculate_score(pred_grid, actual_grid, grid_size=(10, 10)):
    """
    Calculates the score based on the predicted and actual grid numbers.

    Args:
        pred_grid (int): The predicted grid number.
        actual_grid (int): The actual grid number.

    Returns:
        int: The score based on the grid comparison.
    """
    # Calculate the row and column of the predicted and actual grids
    predicted_row = (pred_grid - 1) // grid_size[1]
    predicted_col = (pred_grid - 1) % grid_size[1]
    actual_row = (actual_grid - 1) // grid_size[1]
    actual_col = (actual_grid - 1) % grid_size[1]

    # Calculate the row and column differences
    row_diff = abs(predicted_row - actual_row)
    col_diff = abs(predicted_col - actual_col)

    # Determine the score
    if row_diff == 0 and col_diff == 0:
        score = 3  # Perfect prediction
    elif (row_diff <= 1 and col_diff <= 1):
        score = 2  # Predicted grid is surrounding the actual grid
    elif (row_diff <= 2 and col_diff <= 2) and (row_diff > 1 or col_diff > 1):
        score = 1  # One more layer out (16 neighbors beyond the direct ones)
    else:
        score = 0  # Otherwise
    
    return score

def evaluate_json_folder_with_iou(agent, json_file, dataset_folder, grid_size=(10, 10), checkpoint_file="checkpoint.json"):
    """
    Evaluates the grid-based predictions for images specified in a JSON file using IoU for score 3
    and the original method for scores 2, 1, and 0. Saves intermediate results to a checkpoint file.

    Args:
        agent (RoboCasaAgent): The RoboCasaAgent instance.
        json_file (str): Path to the JSON file containing image data.
        dataset_folder (str): Path to the folder containing the images.
        grid_size (tuple): The size of the grid (rows, columns).
        checkpoint_file (str): Path to the checkpoint file for saving intermediate results.

    Returns:
        list: A list of results with scores for each entry.
    """
    # Load the JSON file
    with open(json_file, "r") as f:
        data = json.load(f)

    # Load existing checkpoint if it exists
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r") as f:
            results = json.load(f)
        processed_images = {entry["image_name"] for entry in results}
        print(f"Resuming from checkpoint. {len(results)} entries already processed.")
    else:
        results = []
        processed_images = set()

    for entry in data:
        image_name = entry["image"]
        description = entry["text"]
        bbox = entry["bbox"]  # {x, y, w, h}

        # Get the image path
        image_path = os.path.join(dataset_folder, image_name)
        agent.image_path = image_path

        try:
            # Get the grid number from the goal description
            grid_number = agent.get_grid_from_goal(goal=description)

            x, y = bbox[0], bbox[1]
            actual_pixel = (x, y)  # Center of the bounding box
            actual_grid = coordinates_to_grid_number(actual_pixel)

            score = calculate_score(grid_number, actual_grid)

            # Append the result
            result = {
                "image_name": image_name,
                "description": description,
                "predicted_grid_number": grid_number,
                "correct_grid_number": actual_grid,
                "score": score
            }
            results.append(result)
            processed_images.add(image_name)

            # Save checkpoint after every 10 entries
            if len(results) % 10 == 0:
                with open(checkpoint_file, "w") as f:
                    json.dump(results, f, indent=4)
                print(f"Checkpoint saved with {len(results)} entries.")

        except Exception as e:
            print(f"Error processing {image_name}: {e}")
            results.append({
                "image_name": image_name,
                "description": description,
                "bounding_box": bbox,
                "error": str(e)
            })

    # Save the final results to a JSON file
    with open("evaluation_results_with_iou.json", "w") as f:
        json.dump(results, f, indent=4)

    print("Evaluation completed. Final results saved.")
    return results

def test_first_entry_with_iou(agent, json_file, dataset_folder, grid_size=(10, 10)):
    """
    Tests the evaluation script on the first entry in the JSON file.

    Args:
        agent (RoboCasaAgent): The RoboCasaAgent instance.
        json_file (str): Path to the JSON file containing image data.
        dataset_folder (str): Path to the folder containing the images.
        grid_size (tuple): The size of the grid (rows, columns).
    """
    # Load the JSON file
    with open(json_file, "r") as f:
        data = json.load(f)

    # Process only the first entry
    entry = data[23]
    image_name = entry["image"]
    description = entry["text"]
    bbox = entry["bbox"]  # {x, y, w, h}

    # Get the image path
    image_path = os.path.join(dataset_folder, image_name)
    agent.image_path = image_path

    try:
        # Get the grid number from the goal description
        grid_number = agent.get_grid_from_goal(goal=description)

        print("grid_number:", grid_number)
        # Convert grid number to pixel coordinates
        predicted_pixel = grid_to_pixel_center(grid_number, grid_size)

        # Convert predicted pixel to bounding box format (center-based)
        grid_width = 225 // grid_size[1]
        grid_height = 225 // grid_size[0]
        predicted_bbox = (
            predicted_pixel[0],
            predicted_pixel[1],
            grid_width,
            grid_height,
        )

        # Calculate IoU
        iou = calculate_iou(bbox, predicted_bbox)

        # Determine the score
        if iou > 0:
            score = 3  # High IoU
        else:
            # Use the original method for scores 2, 1, and 0
            x, y, w, h = bbox[0], bbox[1], bbox[2], bbox[3]
            actual_pixel = (x, y)  # Center of the bounding box
            actual_grid = coordinates_to_grid_number(actual_pixel, grid_size)

            score = calculate_score(grid_number, actual_grid)

        # Print the results for the first entry
        print("Testing First Entry:")
        print(f"Image Name: {image_name}")
        print(f"Description: {description}")
        print(f"Bounding Box: {bbox}")
        print(f"Predicted Grid Number: {grid_number}")
        print(f"Correct Grid Number: {coordinates_to_grid_number((bbox[0], bbox[1]))}")
        print(f"Predicted Pixel: {predicted_pixel}")
        print(f"Predicted Bounding Box: {predicted_bbox}")
        print(f"IoU: {iou}")
        print(f"Score: {score}")

    except Exception as e:
        print(f"Error processing {image_name}: {e}")

if __name__ == "__main__":
    json_file = "C:/Users/ahziy/robocasa/robocasa/dataset/train_dataset.json"
    dataset_folder = "C:/Users/ahziy/OneDrive/Y4S1/FYP/ViLT/vilt/data/images"
    checkpoint_file = "checkpoint.json"

    agent_instance = agent.RoboCasaAgent(image_path="")
    evaluate_json_folder_with_iou(agent_instance, json_file, dataset_folder, checkpoint_file=checkpoint_file)