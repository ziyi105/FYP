import agent

agent = agent.RoboCasaAgent("")
print("Agent initialized successfully.")
print("-----------------------------------------------------")

command = input("Enter an instruction (or 'exit' to quit): ")
scene_path = input("Enter the scene path: ")


print("-----------------------------------------------------")
print("Breaking down instruction with LLM...")
agent.image_path = scene_path
action_plan = agent.generate_action_template(command)
print("-----------------------------------------------------")
print("Action plan generated successfully.")
print("Action plan:", action_plan)
print("-----------------------------------------------------")
print("Translating text descriptions to exact coordinates...")
action_plan = agent.generate_action_dict_with_coordinates(action_plan)
print("-----------------------------------------------------")
print("Coordinates generated successfully.")
print("Action plan with coordinates:", action_plan)
print("Executing the instruction...")
