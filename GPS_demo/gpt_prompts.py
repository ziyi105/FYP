# To generate action plan
user_input_1 = "Clean the kitchen"
generate_action_template = '''
                    Guide the robot to move the chair placed in the wrong place to where it belongs in the kitchen using step-by-step instructions within a specified template. The image provided is a bird-view scene of the kitchen. First, identify the chair needed to be moved and the where is the its correct placement position. Use the following predefined actions to structure your instructions. For every instruction, provide the goal position of the robot (if it's a moving action) or goal position of the object (if it's an object placement or retrieve task). Categorize the actions with their sub-goal. The first set of actions can be to navigate to the chair, the second set to grab the chair and navigate to where it belongs and put it down. Respond in JSON format with the following fields:
                    - "action": The type of action (only "Walk", "Grab" or "Place").
                    - "parameters": Any parameters associated with the action (e.g., direction, object name).
                    - "goal": describe where the robot should end up to be, be specific and you can use nearby fixtures as reference

                    Example output:
                    [
                    {
                        "action": "Walk",
                        "parameters": {
                        "target": "chair"
                        },
                        "goal": add description
                    },
                    {
                        "action": "Grab",
                        "parameters": {
                        "target": "cup"
                        },
                        "goal": "None (target object is specified)."
                    }
                    ]

                    # Notes
                    - Ensure that each instruction leads logically to the next for smooth execution.
                    - Assume the robot can recognize objects and fixtures as named.
                    - Adapt the instructions as necessary for different kitchen layouts.'''

# To infer the goal position
system_prompt_2 = "This is a bird view of a kitchen scene. The green lines are grid and there are numbers in the grid to help you identify them. I will provide a text description of a specific location in the scene. Your task is to determine which grid cell best matches the description. Consider the spatial relationships and any nearby landmarks mentioned in the description. Respond with only the grid number that best matches the description. Do not include any additional text or explanations in your response."