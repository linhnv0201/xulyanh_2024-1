import cv2
import numpy as np
import tkinter as tk
from tkinter import Button, Label, filedialog, Frame
from PIL import Image, ImageTk

# Hàm đọc ảnh
def load_image(path):
    image = cv2.imread(path)
    if image is None:
        print("Error: Could not read image.")
        return None
    return image

# Hàm phát hiện biên bằng Prewitt trên ảnh màu
def prewitt_edge_detection_color(image):
    kernelx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
    channels = cv2.split(image)
    edges = []
    for channel in channels:
        prewitt_x = cv2.filter2D(channel, -1, kernelx)
        prewitt_y = cv2.filter2D(channel, -1, kernely)
        edges.append(prewitt_x + prewitt_y)
    return cv2.merge(edges)

# Hàm phát hiện biên bằng Sobel trên ảnh màu
def sobel_edge_detection_color(image, ksize=3):
    channels = cv2.split(image)
    edges = []
    for channel in channels:
        sobel_x = cv2.Sobel(channel, cv2.CV_64F, 1, 0, ksize=ksize)
        sobel_y = cv2.Sobel(channel, cv2.CV_64F, 0, 1, ksize=ksize)
        magnitude = cv2.magnitude(sobel_x, sobel_y)
        edges.append(np.uint8(magnitude))
    return cv2.merge(edges)

# Hàm phát hiện biên bằng Canny trên ảnh màu
def canny_edge_detection_color(image, low_threshold=50, high_threshold=150):
    channels = cv2.split(image)
    edges = []
    for channel in channels:
        edges.append(cv2.Canny(channel, low_threshold, high_threshold))
    return cv2.merge(edges)

# Hàm hiển thị ảnh với chú thích
def display_with_caption(cv_images, captions):
    # Xóa nội dung cũ
    for widget in display_frame.winfo_children():
        widget.destroy()
    
    # Hiển thị từng ảnh với chú thích
    for i, (cv_image, caption) in enumerate(zip(cv_images, captions)):
        # Resize ảnh để hiển thị
        height, width = cv_image.shape[:2]
        scale = 200 / height  # Resize dựa trên chiều cao tối đa
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized_image = cv2.resize(cv_image, (new_width, new_height))
        
        # Chuyển đổi ảnh cho Pillow
        if len(cv_image.shape) == 3:  # Ảnh màu
            resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(resized_image)
        imgtk = ImageTk.PhotoImage(image=img)
        
        # Label hiển thị ảnh
        img_label = Label(display_frame, image=imgtk)
        img_label.imgtk = imgtk
        img_label.grid(row=0, column=i, padx=10, pady=5)
        
        # Label chú thích
        caption_label = Label(display_frame, text=caption, font=("Arial", 10))
        caption_label.grid(row=1, column=i, padx=10)

# Hàm cập nhật và hiển thị kết quả so sánh
def update_comparison():
    if image is None:
        return
    
    # Áp dụng các bộ phát hiện biên
    prewitt_edges = prewitt_edge_detection_color(image)
    sobel_edges = sobel_edge_detection_color(image, sobel_scale.get())
    canny_edges = canny_edge_detection_color(image, canny_low_scale.get(), canny_high_scale.get())
    
    # Danh sách ảnh và chú thích
    images = [image, prewitt_edges, sobel_edges, canny_edges]
    captions = ["Original Image", "Prewitt Edges", "Sobel Edges", "Canny Edges"]
    
    # Hiển thị ảnh với chú thích
    display_with_caption(images, captions)

# Hàm mở cửa sổ chọn ảnh
def open_image():
    global image
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if file_path:
        image = load_image(file_path)
        if image is not None:
            update_comparison()

# Tạo giao diện chính
root = tk.Tk()
root.title("Edge Detection Comparison with Captions")
root.geometry("1200x600")

# Frame điều khiển
control_frame = tk.Frame(root)
control_frame.pack(fill=tk.BOTH, padx=10, pady=10)

# Frame hiển thị ảnh
display_frame = Frame(root)
display_frame.pack(fill=tk.BOTH, padx=10, pady=10)

# Nút chọn ảnh
open_button = Button(control_frame, text="Open Image", command=open_image)
open_button.grid(row=0, column=0, padx=10)

# Tham số Sobel kernel size
Label(control_frame, text="Sobel Kernel Size:").grid(row=1, column=0, padx=10)
sobel_scale = tk.Scale(control_frame, from_=3, to=11, resolution=2, orient=tk.HORIZONTAL, command=lambda x: update_comparison())
sobel_scale.set(3)
sobel_scale.grid(row=2, column=0, padx=10)

# Tham số Canny thresholds
Label(control_frame, text="Canny Low Threshold:").grid(row=3, column=0, padx=10)
canny_low_scale = tk.Scale(control_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=lambda x: update_comparison())
canny_low_scale.set(50)
canny_low_scale.grid(row=4, column=0, padx=10)

Label(control_frame, text="Canny High Threshold:").grid(row=5, column=0, padx=10)
canny_high_scale = tk.Scale(control_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=lambda x: update_comparison())
canny_high_scale.set(150)
canny_high_scale.grid(row=6, column=0, padx=10)

# Khởi động giao diện
root.mainloop()
