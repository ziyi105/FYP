import os
import json
# from openai import OpenAI
import utils
import gpt_prompts
import base64
import openai
import cv2

class RoboCasaAgent:
    """
    A class to interact with the RoboCasa system and generate step-by-step instructions
    for guiding a robot to perform tasks in a kitchen environment.
    """
    def __init__(self, image_path, model="gpt-4o"):
        """
        Initializes the RoboCasaAgent with the given API key and model.

        Args:
            api_key (str): The API key for accessing the OpenAI service.
            model (str): The model to use for generating instructions. Default is "gpt-4o".
        """
        self.image_path = image_path
        self.model = model
        openai.api_key = "your-api-key"
    def generate_action_template(self, user_input):
        """
        Generates a template of actions for the robot based on user input and an image.

        Args:
            user_input (str): The task description provided by the user.
            image_path (str): The file path to the image of the kitchen scene.

        Returns:
            str: The response message containing the generated action template.
        """
        with open(self.image_path, "rb") as image_file:
            temp_image_path = base64.b64encode(image_file.read()).decode("utf-8")

        messages = [
            {
                "role": "system",
                "content": gpt_prompts.generate_action_template
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_input},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{temp_image_path}"
                        }
                    }
                ]
            }
        ]

        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            response_format={"type": "text"},
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return completion.choices[0].message.content
    
    def get_grid_from_goal(self, goal):
        image_path_with_grids = utils.draw_numbered_grid(self.image_path, (10, 10))
        # Save the image with grids to a temporary file
        temp_image_path = "temp_image_with_grids.jpeg"
        cv2.imwrite(temp_image_path, image_path_with_grids)

        with open(temp_image_path, "rb") as image_file:
            temp_image_path = base64.b64encode(image_file.read()).decode("utf-8")
        messages = [
            {
                "role": "system",
                "content": gpt_prompts.system_prompt_2
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": goal},
                    {
                        "type": "image_url", 
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{temp_image_path}"
                            }
                    },
                ]
            }
        ]

        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            response_format={"type": "text"},
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return utils.extract_grid(completion.choices[0].message.content)


    def generate_action_dict_with_coordinates(self, action_dict):
        """
        Processes the action dictionary and converts spatial descriptions into pixel coordinates.

        Args:
            action_dict (dict): A dictionary where keys are unique action names (e.g., "Walk_1", "Walk_2")
                                and values are goals.

        Returns:
            dict: A dictionary with updated goals as pixel coordinates for "Walk" actions.
        """
        updated_action_dict = {}

        for action, goal in action_dict.items():
            if action.startswith("Walk"):  # Check if the action is a "Walk" action
                print(f"Processing '{action}' with goal: {goal}")
                grid_number = self.get_grid_from_goal(goal)

                goal_pixel_coor = utils.grid_to_pixel_center(grid_number)
                print(f"Predicted Grid number: {grid_number}")
                print(f"Goal pixel coordinates: {goal_pixel_coor}")

                updated_action_dict[action] = goal_pixel_coor
            else:
                # For non-"Walk" actions, copy them as-is
                updated_action_dict[action] = goal

        return updated_action_dict
                
        

    def generate_instructions(self):
        """
        Generates step-by-step instructions for the robot to perform a task.

        Args:
            user_input (str): The task description provided by the user.
            image_path (str): The file path to the image of the kitchen scene.

        Returns:
            dict: A dictionary where the key is the action (e.g., "Walk", "Grab", "Place")
                  and the value is the object or goal position.

        Raises:
            RuntimeError: If valid instructions cannot be generated after 5 attempts.
        """
        max_attempts = 5
        valid_actions = {"Walk", "Grab", "Place"}
        print("Agent initialized successfully.")
        print("-----------------------------------------------------")
        for attempt in range(max_attempts):
            user_input = input("Enter user instruction: ")
            image_path = input("Enter the scene path: ")
            print("-----------------------------------------------------")
            print("Breaking down instruction with LLM...")
            self.image_path = image_path
            response = self.generate_action_template(user_input)
            print("Action plan generated successfully.")
            try:
                json_text = utils.extract_json_from_response(response)
                actions = json.loads(json_text)
                print("Action plan:", json_text)

                print("-----------------------------------------------------")
                print("Translating spatial descriptions to exact coordinates...")
                for step in actions:
                    action = step.get("action")
                    if action not in valid_actions:
                        raise ValueError(f"Invalid action: {action}")

                from collections import defaultdict

                action_dict = {}
                for index, step in enumerate(actions):
                    action = step["action"]
                    if action == "Walk":
                        goal = step.get("goal")
                    else:
                        goal = step.get("parameters", {}).get("target", step.get("goal"))
                    unique_action_name = f"{action}_{index + 1}"
                    action_dict[unique_action_name] = goal

                action_dict_with_coordinates = self.generate_action_dict_with_coordinates(action_dict)
                print("All spatial descriptions translated successfully.")
                print("Action plan with coordinates:", action_dict_with_coordinates)
                print("-----------------------------------------------------")
                print("Executing the instruction...")
                return action_dict_with_coordinates
            
            except (ValueError, json.JSONDecodeError) as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                continue

        raise RuntimeError("Failed to generate valid instructions after 5 attempts.")
        

# Example usage
if __name__ == "__main__":
    agent = RoboCasaAgent("")

    agent.generate_instructions()