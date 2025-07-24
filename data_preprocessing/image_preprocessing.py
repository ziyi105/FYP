import cv2

ref_point = []
cropping = False

def click_and_crop(event, x, y, flags, param):
    """Mouse callback function to select bounding box"""
    global cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        ref_point.append((x, y))
        cropping = False

image = cv2.imread("C:/Users/ahziy/robocasa/robocasa\captured_views\scene_116.png")
clone = image.copy()
cv2.namedWindow("Select Cropping Region")
cv2.setMouseCallback("Select Cropping Region", click_and_crop)

while True:
    cv2.imshow("Select Cropping Region", image)
    key = cv2.waitKey(1) & 0xFF

    # Press 'r' to reset selection
    if key == ord("r"):
        image = clone.copy()

    # Press 'c' to confirm selection and print coordinates
    elif key == ord("c"):
        break

cv2.destroyAllWindows()

if len(ref_point) == 2:
    x1, y1 = ref_point[0]
    x2, y2 = ref_point[1]
    cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2)
    cv2.imshow("Select Cropping Region", image)
    print(f"Cropping coordinates: x1={x1}, y1={y1}, x2={x2}, y2={y2}")

crop_regions = {
    "layout_2": (x1, y1, x2, y2)
}

FIXED_SIZE = (224, 224) 

def crop_and_resize(image_path, layout_name, output_path):
    """Crops image based on layout and resizes it to a fixed size"""
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error loading {image_path}")
        return

    if layout_name in crop_regions:
        x1, y1, x2, y2 = crop_regions[layout_name]
        cropped_img = img[y1:y2, x1:x2]
        resized_img = cv2.resize(cropped_img, FIXED_SIZE, interpolation=cv2.INTER_AREA)
        cv2.imwrite(output_path, resized_img)
        print(f"Saved: {output_path}")
    else:
        print(f"No crop region found for {layout_name}")

folder = "C:/Users/ahziy/robocasa/robocasa/captured_views" 
image_files = [f"scene_{i}.png" for i in range(116, 148)]
layout_name = "layout_2" 

for image_file in image_files:
    crop_and_resize(f"{folder}/{image_file}", layout_name, f"C:/Users/ahziy/robocasa/robocasa/cropped_images/cropped_{image_file}")
