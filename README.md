# FacialAttendance_AWS-Integrated
 
## Overview
This system simplifies attendance management by using facial recognition technology. Registered users are recognized in real-time, their attendance is logged locally in .csv format, and the records are uploaded to AWS S3 for secure storage. Attendance can be viewed through a Streamlit-based dashboard or a responsive HTML interface.

## Features
Face Registration: Use add_faces.py to register faces with unique PINs.
Real-time Attendance: test.py marks attendance and logs it locally and on AWS.
Data Visualization: View attendance data through Streamlit (app.py) or a dynamic HTML table (attendance.html).
Cloud Storage: Upload and manage attendance records using AWS S3.
Search and Filter: Search attendance records by PIN for faster access.
Technologies Used
### Python Modules:
cv2: Face detection and processing.
pickle: Serialize and deserialize data for user storage.
numpy: Numerical operations and data manipulation.
pandas: Handle and process CSV data.
streamlit: Dashboard for attendance visualization.
sklearn.neighbors: K-Nearest Neighbors for facial recognition.
boto3: Integration with AWS S3 for cloud storage.
win32com.client: Text-to-speech functionality for alerts.
### AWS Services:
S3: Secure storage for attendance files.
## How It Works
### Face Registration (add_faces.py):
Users register by entering their name and PIN.
Face images are captured, processed, and stored using OpenCV and NumPy.
User data is serialized with pickle.

### Attendance Marking (test.py):
Detect and recognize faces in real-time using OpenCV and scikit-learn's KNN algorithm.
Log attendance in .csv format and upload it to AWS S3.
Data Visualization:

### Streamlit (app.py): 
View and filter attendance records in an intuitive dashboard.
### HTML (attendance.html): 
Search and view records in a user-friendly table format.

