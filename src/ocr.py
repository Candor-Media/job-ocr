# https://www.youtube.com/watch?v=W9oRTI6mLnU
# https://www.geeksforgeeks.org/feature-matching-using-brute-force-in-opencv/

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import sys
from PIL import Image
import pytesseract
import argparse
import cv2
import numpy as np
from utils import rotate_image

INPUT_IMG_FILENAME = '12th_MARKSHEET.JPG'
UPLOAD_FOLDER = './src/static/uploads'
OUTPUT_FILENAME = '_ocr_output.txt'
GOOD_MATCHES_RATIO = 0.01

filepath = os.path.join(UPLOAD_FOLDER,INPUT_IMG_FILENAME)
print("filepath: " + filepath)

''' Load Source & Target Images '''
# load the example image and convert it to grayscale
image = cv2.imread(filepath)
targetImage = rotate_image(image, 10)
# cv2.imwrite(os.path.join(UPLOAD_FOLDER, '_image.png'), image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
h, w = gray.shape
# gray = cv2.resize(gray, (w//3, h//3))
# cv2.imwrite(os.path.join(UPLOAD_FOLDER, '_gray.png'), gray)

''' Create ORB '''
orb = cv2.ORB_create(10000)
kp1, des1 = orb.detectAndCompute(image, None)
impKp1 = cv2.drawKeypoints(image, kp1, None)
cv2.imwrite(os.path.join(UPLOAD_FOLDER, '_impKp1.png'), impKp1)
kp2, des2 = orb.detectAndCompute(targetImage, None)
impKp2 = cv2.drawKeypoints(targetImage, kp2, None)
cv2.imwrite(os.path.join(UPLOAD_FOLDER, '_impKp2.png'), impKp2)

''' Compute Matches '''
bf = cv2.BFMatcher(cv2.NORM_HAMMING)
matches = bf.match(des1, des2)
print('Nbr of matches: ' + str(len(matches)))
sorted_matches = sorted(matches, key=lambda x: x.distance)
good_matches = sorted_matches[:int(len(matches) * GOOD_MATCHES_RATIO)]
print('Nbr of good matches: ' + str(len(good_matches)))
[print('Distance: ' + str(x.distance)) for x in good_matches]

''' Draw Matches '''
imgMatch = cv2.drawMatches(targetImage, kp2, image, kp1, good_matches, None, flags=2)
cv2.imwrite(os.path.join(UPLOAD_FOLDER, '_imgMatch.png'), imgMatch)

''' Compute Transform Matrix '''
srcPoints = np.float32([kp2[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
dstPoints = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)

M, _ = cv2.findHomography(srcPoints, dstPoints, cv2.RANSAC, 5.0)
# print('M:')
# print(M)

''' Transform Target Image '''
imgScan = cv2.warpPerspective(targetImage, M, (w, h))
cv2.imwrite(os.path.join(UPLOAD_FOLDER, '_imgScan.png'), imgScan)

''' Perform OCR '''
# # apply thresholding to preprocess the image
# imgScan = cv2.threshold(imgScan, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# # apply median blurring to remove any blurring
# imgScan = cv2.medianBlur(imgScan, 3)

# # # save the processed image in the /static/uploads directory
# # ofilename = os.path.join(UPLOAD_FOLDER,"{}.png".format(os.getpid()))
# # cv2.imwrite(ofilename, imgScan)

# # perform OCR on the processed image
# # text = pytesseract.image_to_string(Image.open(ofilename))
print('Starting OCR...')
text = pytesseract.image_to_string(imgScan)

# # remove the processed image
# os.remove(ofilename)

# save the processed image in the /static/uploads directory
# print('Text:')
# print(text)
print('Output text file: ' + OUTPUT_FILENAME)
text_file_name = os.path.join(UPLOAD_FOLDER, OUTPUT_FILENAME)
text_file = open(text_file_name, "w+")
text_file.write(text)
text_file.close()
