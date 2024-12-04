import cv2
import numpy as np
import tkinter as tk
from tkinter import Scale, Button, Label, filedialog
from PIL import Image, ImageTk

# Hàm đọc ảnh và chuyển sang ảnh xám
def load_image(path):
    image = cv2.imread(path)
    if image is None:
        print("Error: Could not read image.")
        return None, None
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
    if cv_image is None:
        return  # Nếu ảnh không hợp lệ, không hiển thị gì.
    
    # Resize the image to fit the window
    max_width = root.winfo_width() - 50  # Maximum width for the display (window width minus padding)
    max_height = root.winfo_height() - 150  # Maximum height for the display (window height minus padding)
    
    height, width = cv_image.shape[:2]
    scale = min(max_width / width, max_height / height)
    
    # Tính toán tỷ lệ và kích thước mới
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    # Resize ảnh
    resized_image = cv2.resize(cv_image, (new_width, new_height))
    img = Image.fromarray(resized_image)
    imgtk = ImageTk.PhotoImage(image=img)
    display_label.imgtk = imgtk
    display_label.configure(image=imgtk)

# Hàm cập nhật kết quả dựa trên các tham số người dùng chọn
def update_image():
    if image is None or gray_image is None:
        return  # Nếu chưa có ảnh, không thực hiện gì
    
    method = method_var.get()
    if method == "Color Image":
        display_image(image)
    elif method == "Gray Image":
        display_image(gray_image)
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

# Hàm mở cửa sổ chọn ảnh
def open_image():
    global image, gray_image
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if file_path:
        image, gray_image = load_image(file_path)
        if image is not None and gray_image is not None:
            update_image()  # Cập nhật ảnh ngay khi ảnh đã được tải thành công
        else:
            print("Failed to load image.")

# Tạo giao diện chính
root = tk.Tk()
root.title("Edge Detection Application")

# Thiết lập kích thước cửa sổ
root.geometry("900x700")  # Đặt kích thước cửa sổ chính

# Tạo một Frame để chứa các nút và thanh trượt
control_frame = tk.Frame(root)
control_frame.pack(fill=tk.BOTH, padx=10, pady=10)

# Label để hiển thị ảnh
display_label = Label(root)
display_label.pack(pady=20)

# Thêm nút chọn ảnh
open_button = Button(control_frame, text="Open Image", command=open_image)
open_button.grid(row=0, column=0, padx=10)

# Chọn bộ phát hiện biên
method_var = tk.StringVar(value="Color Image")
Label(control_frame, text="Select Edge Detection Method:").grid(row=1, column=0, padx=10)
tk.Radiobutton(control_frame, text="Color Image", variable=method_var, value="Color Image", command=update_image).grid(row=2, column=0, sticky="w")
tk.Radiobutton(control_frame, text="Gray Image", variable=method_var, value="Gray Image", command=update_image).grid(row=3, column=0, sticky="w")
tk.Radiobutton(control_frame, text="Prewitt", variable=method_var, value="Prewitt", command=update_image).grid(row=4, column=0, sticky="w")
tk.Radiobutton(control_frame, text="Sobel", variable=method_var, value="Sobel", command=update_image).grid(row=5, column=0, sticky="w")
tk.Radiobutton(control_frame, text="Canny", variable=method_var, value="Canny", command=update_image).grid(row=6, column=0, sticky="w")

# Tham số Sobel kernel size
Label(control_frame, text="Sobel Kernel Size").grid(row=7, column=0, padx=10)
sobel_scale = Scale(control_frame, from_=3, to=11, resolution=2, orient=tk.HORIZONTAL, command=lambda x: update_image())
sobel_scale.set(3)
sobel_scale.grid(row=8, column=0, padx=10, pady=10)

# Tham số Canny thresholds
Label(control_frame, text="Canny Low Threshold").grid(row=9, column=0, padx=10)
canny_low_scale = Scale(control_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=lambda x: update_image())
canny_low_scale.set(50)
canny_low_scale.grid(row=10, column=0, padx=10, pady=10)

Label(control_frame, text="Canny High Threshold").grid(row=11, column=0, padx=10)
canny_high_scale = Scale(control_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=lambda x: update_image())
canny_high_scale.set(150)
canny_high_scale.grid(row=12, column=0, padx=10, pady=10)

# Khởi động giao diện
root.mainloop()
