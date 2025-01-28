import pytesseract
import os
from PIL import Image
import tempfile
import pygame
import cv2
import datetime

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Set the path to Tesseract executable
pygame.init()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\tesseract\tesseract.exe"

def process_image(image_path, language):
    '''Takes an image path and language code, returns the text in the image'''
    # Read image data from the local file
    with open(image_path, 'rb') as img_file:
        img_data = img_file.read()
    
    # Save image data to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_img_file:
        temp_img_file.write(img_data)
        temp_img_file_path = temp_img_file.name
    
    # Extract text from the image using Tesseract OCR
    text = pytesseract.image_to_string(Image.open(temp_img_file_path), lang=language)
    
    # Delete the temporary file
    os.unlink(temp_img_file_path)
    
    return text

def repair(text):
    '''Removes and replaces likely mistaken chars'''
    return text.replace("|", "I").replace("\n", " ")

def write_text_to_file(text):
    with open("NumberPlate.txt", "a") as file:
        file.write(text)

def read_text_from_file(loc):
    with open(loc, "r") as file:
        return file.read()
    
def get_current_time():
    current_time = datetime.datetime.now()
    return current_time
    
def capture_photo():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Couldn't open the camera")
        return
    ret, frame = cap.read()
    # Check if the frame is captured successfully
    if not ret:
        print("Error: Couldn't capture frame")
        return

    # Save the captured frame as an image
    cv2.imwrite("captured_photo.jpg", frame)

    # Release the camera capture object
    cap.release()

    print("Photo captured successfully")

# Test your functions
capture_photo()
processed_text = repair(process_image("captured_photo.jpg", "eng"))
current_time = str(get_current_time())
write_text_to_file("car with registration number \t" + processed_text + "\t entered at time \t" + current_time +"\n")

