import json

def process_evaluation_results(json_file):
    """
    Processes the evaluation results JSON file to calculate the average score
    and the number of cases for each score.

    Args:
        json_file (str): Path to the JSON file containing evaluation results.

    Returns:
        dict: A dictionary containing the average score and score distribution.
    """
    # Load the JSON file
    with open(json_file, "r") as f:
        data = json.load(f)

    # Initialize variables
    total_score = 0
    score_counts = {0: 0, 1: 0, 2: 0, 3: 0}
    total_cases = 0

    # Process each entry in the JSON file
    for entry in data:
        if "score" in entry:
            score = entry["score"]
            total_score += score
            score_counts[score] += 1
            total_cases += 1

    # Calculate the average score
    average_score = total_score / total_cases if total_cases > 0 else 0

    # Print the results
    print("Evaluation Results Summary:")
    print(f"Average Score: {average_score:.2f}")
    print("Score Distribution:")
    for score, count in score_counts.items():
        print(f"  Score {score}: {count} cases")

    # Return the results as a dictionary
    return {
        "average_score": average_score,
        "score_distribution": score_counts
    }

# Example usage
if __name__ == "__main__":
    json_file = "checkpoint.json"
    print(process_evaluation_results(json_file))