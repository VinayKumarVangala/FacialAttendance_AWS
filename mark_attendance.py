from sklearn.neighbors import KNeighborsClassifier 
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch
import boto3

def speak(str1):
    speak = Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

# AWS credentials
BUCKET_NAME = 'facial-attendance-system'
ACCESS_KEY = 'AKIAQMZHWNDKDRRE5GEY'
SECRET_ACCESS_KEY = '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'

# Boto3 S3 client setup
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_ACCESS_KEY)

video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

with open('data/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)
with open('data/pins.pkl', 'rb') as p:  # Load the PINs
    PINS = pickle.load(p)
print('Shape of Faces matrix --> ', FACES.shape)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

imgBackground = cv2.imread("background.png")

# Set up CSV for today's attendance
COL_NAMES = ['S.no', 'Name', 'Time', 'Date', 'PIN']  # Removed UniqueID, Added PIN
attendance_list = []
unique_id = 1
date = datetime.now().strftime("%d-%m-%Y")

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)
        ts = time.time()
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(output[0]), (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

        pin = PINS[LABELS.index(output[0])]  # Retrieve PIN using the name

    imgBackground[162:162 + 480, 55:55 + 640] = frame
    cv2.imshow("Frame", imgBackground)

    # Capture and store attendance only when 'p' is pressed
    k = cv2.waitKey(1)
    if k == ord('p'):  # Mark attendance only when 'p' is pressed
        attendance = [str(unique_id), str(output[0]), str(timestamp), str(date), str(pin)]  # Use the PIN here
        attendance_list.append(attendance)
        
        speak("Attendance Taken..")
        time.sleep(2)
        
        # Change to create a new CSV file for today's date
        file_path = f"Attendance/Attendance_{date}.csv"
        with open(file_path, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            if os.stat(file_path).st_size == 0:  # Check if file is empty
                writer.writerow(COL_NAMES)  # Write column names only if file is empty
            writer.writerow(attendance)  # Write only the current attendance record

        # Upload to AWS S3
        s3.upload_file(file_path, BUCKET_NAME, 'Attendance/' + f"Attendance_{date}.csv")

        unique_id += 1  # Increment unique ID for the next attendance record

    if k == ord('e'):
        break

video.release()
cv2.destroyAllWindows()