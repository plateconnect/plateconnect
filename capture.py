import cv2
import yolov5
import pytesseract # we use this for optical character recognition
from PIL import Image # another image processing library
import math
# load pretrained model

model = yolov5.load('keremberke/yolov5m-license-plate')
searched_plates = []

# set model parameters
model.conf = 0.25  # NMS confidence threshold
model.iou = 0.45  # NMS IoU threshold
model.agnostic = False  # NMS class-agnostic
model.multi_label = False  # NMS multiple labels per box
model.max_det = 1000  # maximum number of detections per image

# set image
img = 'license.png'

# parse results

cap = cv2.VideoCapture(r"C:\Users\austi\Downloads\Untitled video (1).mp4") #replace with video path for cars

while True:
    ret, frame = cap.read()
    result = model(frame)
    predictions = result.pred[0]
    boxes = predictions[:, :4] # x1, y1, x2, y2

    for plate_coords in boxes:
        x1, y1, x2, y2 = map(int, plate_coords)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cropped_image = frame[y1:y2, x1:x2]
        name = "results/cropped" + str(math.floor(x1)) + ".png"
        cv2.imwrite(name, cropped_image)

        # Adding custom options
        custom_config = r'--oem 3 --psm 6'
        plate_number = pytesseract.image_to_string(name, config=custom_config)
        searched_plates.append(plate_number)
        print(plate_number)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
