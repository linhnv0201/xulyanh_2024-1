import cv2
import numpy as np

def load_image(path):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image, gray

image, gray_image = load_image('Image_for_TeamSV\car.jpg')
cv2.imshow('Original Image', image)
cv2.imshow('Gray Image', gray_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
