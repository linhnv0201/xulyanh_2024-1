import cv2
import numpy as np
import tkinter as tk
from tkinter import Scale, Button, Label
from PIL import Image, ImageTk

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

# Hàm phát hiện biên bằng Sobel với kích thước kernel tùy chỉnh
def sobel_edge_detection(gray, ksize):
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
    sobel = cv2.magnitude(sobel_x, sobel_y)
    return np.uint8(sobel)

# Hàm phát hiện biên bằng Canny với ngưỡng tùy chỉnh
def canny_edge_detection(gray, low_threshold, high_threshold):
    return cv2.Canny(gray, low_threshold, high_threshold)

# Hàm hiển thị ảnh trên giao diện
def display_image(cv_image):
    img = Image.fromarray(cv_image)
    imgtk = ImageTk.PhotoImage(image=img)
    display_label.imgtk = imgtk
    display_label.configure(image=imgtk)

# Hàm cập nhật kết quả dựa trên các tham số người dùng chọn
def update_image():
    method = method_var.get()
    if method == "Normal":
        # Hiển thị ảnh gốc nếu chọn "Normal"
        display_image(image)
    elif method == "Prewitt":
        edges = prewitt_edge_detection(gray_image)
        display_image(edges)
    elif method == "Sobel":
        ksize = sobel_scale.get()
        edges = sobel_edge_detection(gray_image, ksize)
        display_image(edges)
    elif method == "Canny":
        low_threshold = canny_low_scale.get()
        high_threshold = canny_high_scale.get()
        edges = canny_edge_detection(gray_image, low_threshold, high_threshold)
        display_image(edges)

# Đường dẫn đến ảnh của bạn
image_path = 'Image_for_TeamSV\car.jpg'
image, gray_image = load_image(image_path)

# Tạo giao diện chính
root = tk.Tk()
root.title("Edge Detection Application")

# Label để hiển thị ảnh
display_label = Label(root)
display_label.pack()

# Chọn bộ phát hiện biên
method_var = tk.StringVar(value="Prewitt")
Label(root, text="Select Edge Detection Method:").pack()
tk.Radiobutton(root, text="Normal", variable=method_var, value="Normal", command=update_image).pack()
tk.Radiobutton(root, text="Prewitt", variable=method_var, value="Prewitt", command=update_image).pack()
tk.Radiobutton(root, text="Sobel", variable=method_var, value="Sobel", command=update_image).pack()
tk.Radiobutton(root, text="Canny", variable=method_var, value="Canny", command=update_image).pack()

# Tham số Sobel kernel size
Label(root, text="Sobel Kernel Size").pack()
sobel_scale = Scale(root, from_=3, to=11, resolution=2, orient=tk.HORIZONTAL, command=lambda x: update_image())
sobel_scale.set(3)
sobel_scale.pack()

# Tham số Canny thresholds
Label(root, text="Canny Low Threshold").pack()
canny_low_scale = Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, command=lambda x: update_image())
canny_low_scale.set(50)
canny_low_scale.pack()

Label(root, text="Canny High Threshold").pack()
canny_high_scale = Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, command=lambda x: update_image())
canny_high_scale.set(150)
canny_high_scale.pack()

# Hiển thị ảnh gốc ban đầu
display_image(gray_image)

# Khởi động giao diện
root.mainloop()
