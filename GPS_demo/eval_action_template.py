import os
import random
import json
from statistics import mean
from agent import RoboCasaAgent 
from utils import validate_action_template, extract_json_from_response

def evaluate_action_template(action_template):
    """
    Evaluates the action template for correctness by asking the user for input.

    Args:
        action_template (str): The generated action template.

    Returns:
        float: A score between 1 and 3 representing the quality of the template.
    """

    print("\nGenerated Action Template:")
    print(action_template)
    while True:
        try:
            score = int(input("Rate the quality of the action template (1 = Poor, 2 = Average, 3 = Excellent): "))
            if score in {0, 1, 2}:
                return score
            else:
                print("Please enter a valid score (0, 1, 2).")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 2.")

def process_scene_images(dataset_folder, sample_size=30):
    """
    Processes a dataset of scene images to generate action templates, evaluate them,
    and record the average correctness score along with the top and lowest scoring images.

    Args:
        dataset_folder (str): The folder containing the dataset of .jpeg images.
        sample_size (int): The number of images to randomly sample from the dataset.

    Returns:
        dict: A summary containing the average scores, top-scoring images, and lowest-scoring images.
    """
    # Get all .jpeg images in the dataset folder
    all_images = [os.path.join(dataset_folder, f) for f in os.listdir(dataset_folder) if f.endswith('.jpeg')]

    # Randomly sample 30 images
    sampled_images = random.sample(all_images, min(sample_size, len(all_images)))

    # Initialize the RoboCasaAgent
    agent = RoboCasaAgent(image_path=None)  # Image path will be set dynamically

    # Store scores and results
    validation_scores = []
    human_scores = []
    results = []

    for image_path in sampled_images:
        print(f"Processing image: {image_path}")
        agent.image_path = image_path  # Set the image path dynamically

        # Generate action template
        try:
            # Ensure the correct type is passed to the API
            response = agent.generate_action_template()  # Replace 'image_file' with 'file'
            # Validate the action template format
            is_valid = validate_action_template(response)
            validation_score = 1 if is_valid else 0
            validation_scores.append(validation_score)

            action_template = extract_json_from_response(response)
            # Evaluate the action template quality
            human_score = evaluate_action_template(action_template)
            human_scores.append(human_score)

            # Record the result
            results.append({
                "image": image_path,
                "validation_score": validation_score,
                "human_score": human_score,
                "action_template": action_template
            })
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            continue

    # Calculate average scores
    average_validation_score = mean(validation_scores) if validation_scores else 0
    average_human_score = mean(human_scores) if human_scores else 0

    # Sort results by human score
    results.sort(key=lambda x: x["human_score"], reverse=True)

    # Get top 3 and lowest 3 scoring images
    top_images = results[:3]
    lowest_images = results[-3:]

    # Count images with the highest score for both metrics
    highest_score_count = sum(
        1 for result in results if result["validation_score"] == 1 and result["human_score"] == 2
    )

    # Summary
    summary = {
        "average_validation_score": average_validation_score,
        "average_human_score": average_human_score,
        "highest_score_count": highest_score_count,
        "top_images": top_images,
        "lowest_images": lowest_images
    }

    # Save the summary to a JSON file
    with open("evaluation_summary.json", "w") as f:
        json.dump(summary, f, indent=4)

    print(f"Average Validation Score: {average_validation_score}")
    print(f"Average Human Score: {average_human_score}")
    print(f"Number of images with highest scores for both metrics: {highest_score_count}")
    print("Top Scoring Images:")
    for item in top_images:
        print(f"Image: {item['image']}, Validation Score: {item['validation_score']}, Human Score: {item['human_score']}")

    print("Lowest Scoring Images:")
    for item in lowest_images:
        print(f"Image: {item['image']}, Validation Score: {item['validation_score']}, Human Score: {item['human_score']}")

    return summary

# Example usage
if __name__ == "__main__":
    dataset_folder = "C:/Users/ahziy/OneDrive/Y4S1/FYP/ViLT/vilt/data/images"  # Replace with the path to your dataset folder
    process_scene_images(dataset_folder)