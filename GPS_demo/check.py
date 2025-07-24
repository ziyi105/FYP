import agent
import utils
import cv2

ori_img = "C:/Users/ahziy/OneDrive/Y4S1/FYP/ViLT/vilt/data/images/cropped_scene_1.jpeg"
# agent = agent.RoboCasaAgent("C:/Users/ahziy/OneDrive/Y4S1/FYP/ViLT/vilt/data/images/cropped_scene_1.jpeg")
# predicted_grid_number = agent.get_grid_from_goal("to the right of the middle chair")
# print("predicted_grid_number:", predicted_grid_number)

# print("correct grid number: ", utils.coordinates_to_grid_number((147+7, 147+7)))
# img = utils.draw_numbered_grid("C:/Users/ahziy/robocasa/robocasa/annotated_images/train_dataset/cropped_scene_1_cross_1_bbox.jpeg")
# # cv2.imshow("img", img)
# # cv2.waitKey(0)

# image = cv2.circle(img, (143, 121), radius=1, color=(0, 0, 255), thickness=-1)
# cv2.imshow("image", image)
# cv2.waitKey(0)

# print(utils.grid_to_pixel_center(67))

print(utils.coordinates_to_grid_number((147, 147)))