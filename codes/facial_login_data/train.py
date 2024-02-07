import os
import math
import numpy as np
from PIL import Image
import cv2
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "data")

os.system("clear")
detail = False

# Load the OpenCV face recognition detector Haar
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
# Create OpenCV LBPH recognizer for training
recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
y_label = []
x_train = []

# Traverse all face images in `data` folder
for root, dirs, files in os.walk(image_dir):
    num_files = len(files)
    count = 0
    for file in files:
        count += 1
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            label = os.path.basename(root).replace("", "").upper()  # name
            if (detail == True): print(label, path)

            if label in label_ids:
                pass
            else:
                label_ids[label] = current_id
                current_id += 1
            id_ = label_ids[label]
            if (detail == True): print(label_ids)

            pil_image = Image.open(path).convert("L")
            image_array = np.array(pil_image, "uint8")
            if (detail == True): print(image_array)
            # Using multiscle detection
            faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

            for (x, y, w, h) in faces:
                roi = image_array[y:y+h, x:x+w]
                x_train.append(roi)
                y_label.append(id_)

            if (not detail): 

                if (count % 5 == 0): 
                    os.system("clear")
                    print("Training in progress ...")
                    name = root.split("/")[-1]
                    progress = 50 * count * 1.0 / num_files
                    print (math.floor(progress) * '#', end="")
                    if (progress != 50):
                        print (str(math.floor(10*(progress - math.floor(progress)))), end="")
                        print ((50 - math.floor(progress) - 1) * '-', end="")
                    print (f"  {count}/{num_files} for {name}")


# labels.pickle store the dict of labels.
# {name: id}  
# id starts from 0
with open("labels.pickle", "wb") as f:
    pickle.dump(label_ids, f)

# Train the recognizer and save the trained model.
os.system("clear")
print("Training the recognizer ...")
recognizer.train(x_train, np.array(y_label))
recognizer.save("train.yml")
os.system("clear")
print("Training FINISHED. \n")