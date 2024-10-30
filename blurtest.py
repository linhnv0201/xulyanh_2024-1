import cv2

# Đọc ảnh từ file
image = cv2.imread('Image_for_TeamSV\car.jpg')

# Kiểm tra xem ảnh có được đọc đúng không
if image is None:
    print("Không thể mở ảnh. Kiểm tra lại đường dẫn.")
else:
    # Áp dụng Gaussian Blur để làm mờ ảnh. Tham số (15, 15) là kích thước của kernel (bộ lọc), và số 0 là giá trị độ lệch chuẩn (sigma) mặc định.
    blurred_image = cv2.GaussianBlur(image, (15, 15), 0)

    # Xoay ngược ảnh 180 độ
    rotated_image = cv2.rotate(image, cv2.ROTATE_180)

    # Hiển thị ảnh gốc và ảnh sau khi làm mờ
    cv2.imshow('Original Image', image)
    cv2.imshow('Blurred Image', blurred_image)
    cv2.imshow('Rotated Image (180 degrees)', rotated_image)
    
    # Đợi phím bất kỳ và đóng cửa sổ hiển thị
    cv2.waitKey(0)
    cv2.destroyAllWindows()
