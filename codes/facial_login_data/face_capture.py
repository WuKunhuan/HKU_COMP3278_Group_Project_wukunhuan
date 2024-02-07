import cv2
import os

os.system("clear")
print("Wait for the face capture to start ... (this may take around 10 seconds)")

faceCascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
video_capture = cv2.VideoCapture(0)

# Specify the `user_name` and `NUM_IMGS` here.
# The user_name should be student_id in string format.
user_name = ""
while (not user_name or os.path.exists('data/{}'.format(user_name))):
    user_name = input("\nUsername: ")
    if (os.path.exists('data/{}'.format(user_name))):
        overwrite = input("User already exists. Are you sure to overwrite? [Y]/n")
        if (overwrite == "Y"): 
            os.system(f"rm -rf data/{user_name}")
            print("User data erased. \n")

num = ""
while(not (num.isnumeric() and int(num) >= 100)): 
    print("\nAround 250 images can be captured within 1 minute. ")
    num = input("Number of images to capture (minimum 100): ")
NUM_IMGS = int(num)

print("\nFace capturing has STARTED ...")
if not os.path.exists('data/{}'.format(user_name)):
    os.system(f"mkdir -p data/{user_name}")

cnt = 1
font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (350, 50)
fontScale = 1
fontColor = (102, 102, 225)
lineType = 2

# Open camera
while cnt <= NUM_IMGS:

    # Capture frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    msg = "Saving {}'s Face Data [{}/{}]".format(user_name, cnt, NUM_IMGS)
    cv2.putText(frame, msg,
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)


    # Display the resulting frame
    cv2.imshow('Video', frame)
    # Store the captured images in `data/Jack`
    cv2.imwrite("data/{}/{}{:03d}.jpg".format(user_name, user_name, cnt), frame)
    cnt += 1

    key = cv2.waitKey(100)

# When everything is done, release the capture

print(f"\nFace capturing FINISHED. User {user_name}'s data has been saved. \n")
video_capture.release()
cv2.destroyAllWindows()
