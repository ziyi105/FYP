import agent
import utils

agent = agent.RoboCasaAgent("C:/Users/ahziy/OneDrive/Y4S1/FYP/ViLT/vilt/data/images/cropped_scene_1.jpeg")
predicted_grid_number = agent.get_grid_from_goal("to the right of the middle chair")
pixel_coordinates = utils.grid_to_pixel_center(predicted_grid_number)

print("pixel_coordinates:", pixel_coordinates)