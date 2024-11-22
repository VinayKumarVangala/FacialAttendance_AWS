
import cv2
import pickle
import numpy as np
import os

video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

faces_data = []
i = 0
name = input("Enter Your Name: ")
pin = input("Enter a PIN number: ")  # New PIN input
max_captures = 20

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50))
        
        # Update condition to 20
        if len(faces_data) < max_captures and i % 10 == 0:
            faces_data.append(resized_img)
        
        i += 1
        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)
    
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    
    # Break after 20 captures
    if k == ord('q') or len(faces_data) == max_captures:
        break

video.release()
cv2.destroyAllWindows()

faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(max_captures, -1)

# Save names, PINs, and faces data with 20 captures
if 'names.pkl' not in os.listdir('data/'):
    names = [name] * max_captures
    pins = [pin] * max_captures  # New: Store the PIN
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)
    with open('data/pins.pkl', 'wb') as f:  # New file for PINs
        pickle.dump(pins, f)
else:
    with open('data/names.pkl', 'rb') as f:
        names = pickle.load(f)
    with open('data/pins.pkl', 'rb') as f:  # Load existing PINs
        pins = pickle.load(f)
    names = names + [name] * max_captures
    pins = pins + [pin] * max_captures  # Add new PINs
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)
    with open('data/pins.pkl', 'wb') as f:  # Save updated PINs
        pickle.dump(pins, f)

if 'faces_data.pkl' not in os.listdir('data/'):
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces_data, f)
else:
    with open('data/faces_data.pkl', 'rb') as f:
        faces = pickle.load(f)
    faces = np.append(faces, faces_data, axis=0)
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces, f)
        
#python add_faces.py