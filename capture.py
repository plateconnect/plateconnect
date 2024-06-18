import cv2
import yolov5
import pytesseract # we use this for optical character recognition
from PIL import Image # another image processing library


# load pretrained model
model = yolov5.load('keremberke/yolov5m-license-plate')

# set model parameters
model.conf = 0.25  # NMS confidence threshold
model.iou = 0.45  # NMS IoU threshold
model.agnostic = False  # NMS class-agnostic
model.multi_label = False  # NMS multiple labels per box
model.max_det = 1000  # maximum number of detections per image

# set image
img = 'main-qimg-dc45532d45e1d8733b3b8bc8f62e8385-lq.jpeg'

image_data = cv2.imread(img)
# perform inference
results = model(img)

# inference with larger input size
results = model(img, size=1280)

# inference with test time augmentation
results = model(img, augment=True)

# parse results
predictions = results.pred[0]
boxes = predictions[:, :4] # x1, y1, x2, y2

for plate_coords in boxes:
    x1, y1, x2, y2 = map(int, plate_coords)
    cropped_image = image_data[y1:y2, x1:x2]
    import math
    name = "cropped" + str(math.floor(x1)) + ".png"
    cv2.imwrite(name, cropped_image)

    # Adding custom options
    custom_config = r'--oem 3 --psm 6'
    plate_number = pytesseract.image_to_string(name, config=custom_config)
    print(plate_number)

scores = predictions[:, 4]
categories = predictions[:, 5]

# show detection bounding boxes on image
results.show()

# save results into "results/" folder
results.save(save_dir='results/')