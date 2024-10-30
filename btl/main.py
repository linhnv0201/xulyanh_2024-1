import cv2
import numpy as np

# Hàm đọc ảnh và chuyển sang ảnh xám
def load_image(path):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image, gray

# Hàm phát hiện biên bằng Prewitt
def prewitt_edge_detection(gray):
    kernelx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
    prewitt_x = cv2.filter2D(gray, -1, kernelx)
    prewitt_y = cv2.filter2D(gray, -1, kernely)
    return prewitt_x + prewitt_y

# Hàm phát hiện biên bằng Sobel
def sobel_edge_detection(gray):
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel = cv2.magnitude(sobel_x, sobel_y)
    return sobel

# Hàm phát hiện biên bằng Canny với điều chỉnh ngưỡng
def canny_edge_detection(gray, low_threshold=100, high_threshold=200):
    return cv2.Canny(gray, low_threshold, high_threshold)

# Hàm hiển thị ảnh
def display_images(images, titles):
    for i in range(len(images)):
        cv2.imshow(titles[i], images[i])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Đọc ảnh và chuyển đổi sang ảnh xám
image_path = 'Image_for_TeamSV\car.jpg'  # Đường dẫn tới ảnh của bạn
image, gray_image = load_image(image_path)

# Áp dụng các bộ phát hiện biên
prewitt_edges = prewitt_edge_detection(gray_image)
sobel_edges = sobel_edge_detection(gray_image)
canny_edges = canny_edge_detection(gray_image, low_threshold=50, high_threshold=150)

# Hiển thị kết quả
display_images(
    [image, gray_image, prewitt_edges, sobel_edges, canny_edges],
    ['Original Image', 'Gray Image', 'Prewitt Edge Detection', 'Sobel Edge Detection', 'Canny Edge Detection']
)
