import re
import cv2
import json


def validate_action_template(response):
    """
    Validates the format of the action template and checks for undefined actions.

    Args:
        action_template (str): The generated action template.

    Returns:
        bool: True if the template is valid, False otherwise.
    """
    try:
        # Extract the JSON block from the response
        json_block = extract_json_from_response(response)
        
        # Parse the action template as JSON
        actions = json.loads(json_block)

        # Check if it's a list of dictionaries
        if not isinstance(actions, list):
            return False

        # Check each action for required fields and valid action types
        valid_actions = {"Walk", "Grab", "Place", "walk", "grab", "place"}
        for action in actions:
            if not isinstance(action, dict):
                return False
            if "action" not in action or "parameters" not in action or "goal" not in action:
                return False
            if action["action"] not in valid_actions:
                return False

        return True
    except json.JSONDecodeError:
        return False

def draw_numbered_grid(img, grid_size=(10, 10)):
    """Draws a grid with numbers starting from 1 at the top-left of the grid, keeping the grid lines visible."""
    img = cv2.imread(img)
    height, width = img.shape[:2]
    cell_width, cell_height = width // grid_size[1], height // grid_size[0]

    grid_img = img.copy()
    number = 1  # Start numbering from 1

    # Draw the grid lines
    for i in range(1, grid_size[0]):
        cv2.line(grid_img, (0, i * cell_height), (width, i * cell_height), (0, 255, 0), 1)
    for j in range(1, grid_size[1]):
        cv2.line(grid_img, (j * cell_width, 0), (j * cell_width, height), (0, 255, 0), 1)

    # Write the numbers in the grid cells
    for i in range(grid_size[0]):  # Rows
        for j in range(grid_size[1]):  # Columns
            # Calculate the center of the current grid cell
            x = j * cell_width + cell_width // 2
            y = i * cell_height + cell_height // 2

            # Adjust the font size and position for better alignment
            font_scale = 0.25  # Smaller font size
            thickness = 1
            text_size = cv2.getTextSize(str(number), cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
            text_x = x - text_size[0] // 2  # Center the text horizontally
            text_y = y + text_size[1] // 2  # Center the text vertically

            # Write the number at the center of the grid cell
            cv2.putText(grid_img, str(number), (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), thickness)
            number += 1
        
    cv2.imwrite("grid_img.jpeg", grid_img)  # Save the image with the grid

    return grid_img

def extract_json_from_response(response): 
    """
    Extracts a JSON block from the response string.

    Args:
        response (str): The response string containing a JSON block.

    Returns:
        str: The extracted JSON block as a string.

    Raises:
        ValueError: If no JSON block is found in the response.
    """
    match = re.search(r"\[.*?\]", response, re.DOTALL) 
    if match: 
        json_text = match.group(0)
        return json_text 
    else: 
        raise ValueError("No JSON block found in the response.")

def extract_grid(response):
    """
    Extracts the grid number from the response string.

    Args:
        response (str): The response string containing a grid number.

    Returns:
        str: The extracted grid number as a string.
    """
    match = re.search(r"\d+", response)
    if match:
        return int(match.group(0))
    else:
        raise ValueError("No grid number found in the response.")
    
def grid_to_pixel_center(grid_number, image_size=(225, 225), grid_size=(10, 10)):
    """
    Calculates the center pixel coordinates of a grid cell based on the grid number.

    Args:
        grid_number (int): The grid number (1-based index).
        image_size (tuple): The size of the image in pixels (width, height). Default is (225, 225).
        grid_size (tuple): The number of grids in the image (rows, columns). Default is (10, 10).

    Returns:
        tuple: The center pixel coordinates (x, y) of the grid cell.
    """
    # Calculate the size of each grid cell in pixels
    cell_width = image_size[0] // grid_size[1]  # Width of each grid cell
    cell_height = image_size[1] // grid_size[0]  # Height of each grid cell

    # Convert the grid number to a 0-based index
    grid_index = grid_number - 1

    # Calculate the row and column of the grid cell
    row = grid_index // grid_size[1]  # Divide by the number of columns
    col = grid_index % grid_size[1]  # Modulus gives the column index

    # Calculate the center pixel coordinates
    center_x = (col * cell_width) + (cell_width // 2)
    center_y = (row * cell_height) + (cell_height // 2)

    return (center_x, center_y)

def coordinates_to_grid_number(coordinates, image_size=(225, 225), grid_size=(10, 10)):
    """
    Converts pixel coordinates to a grid cell number.

    Args:
        coordinates (tuple): The pixel coordinates (x, y).
        image_size (tuple): The size of the image in pixels (width, height). Default is (225, 225).
        grid_size (tuple): The number of grids in the image (columns, rows). Default is (10, 10).

    Returns:
        int: The grid cell number (1-based index).
    """
    x, y = coordinates
    grid_width = image_size[0] // grid_size[1]  # Width of each grid cell
    grid_height = image_size[1] // grid_size[0]  # Height of each grid cell

    # Ensure the coordinates are within the image bounds
    x = max(0, min(x, image_size[0] - 1))
    y = max(0, min(y, image_size[1] - 1))

    # Calculate the column and row indices
    col = x // grid_width
    row = y // grid_height

    # Convert to 1-based grid number
    grid_number = row * grid_size[1] + col + 1
    return grid_number

def calculate_iou(bbox1, bbox2):
    """
    Calculates the Intersection over Union (IoU) between two bounding boxes.

    Args:
        bbox1 (tuple): The first bounding box in (x, y, w, h) format (center-based).
        bbox2 (tuple): The second bounding box in (x, y, w, h) format (center-based).

    Returns:
        float: The IoU value between 0 and 1.
    """
    # Convert center-based format (x, y, w, h) to corner-based format (x_min, y_min, x_max, y_max)
    x1_min = bbox1[0] - bbox1[2] // 2
    y1_min = bbox1[1] - bbox1[3] // 2
    x1_max = bbox1[0] + bbox1[2] // 2
    y1_max = bbox1[1] + bbox1[3] // 2

    x2_min = bbox2[0] - bbox2[2] // 2
    y2_min = bbox2[1] - bbox2[3] // 2
    x2_max = bbox2[0] + bbox2[2] // 2
    y2_max = bbox2[1] + bbox2[3] // 2
    
    # Calculate the intersection coordinates
    inter_x_min = max(x1_min, x2_min)
    inter_y_min = max(y1_min, y2_min)
    inter_x_max = min(x1_max, x2_max)
    inter_y_max = min(y1_max, y2_max)

    # Calculate the area of the intersection
    inter_width = max(0, inter_x_max - inter_x_min)
    inter_height = max(0, inter_y_max - inter_y_min)
    inter_area = inter_width * inter_height

    # Calculate the area of both bounding boxes
    area1 = (x1_max - x1_min) * (y1_max - y1_min)
    area2 = (x2_max - x2_min) * (y2_max - y2_min)

    # Calculate the union area
    union_area = area1 + area2 - inter_area

    # Calculate IoU
    iou = inter_area / union_area if union_area > 0 else 0
    return iou
