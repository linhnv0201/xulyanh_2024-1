import cv2

import numpy as np
import matplotlib.pyplot as plt

# Đọc ảnh từ file
image = cv2.imread('image\cauhoi123.png')


# Kiểm tra xem ảnh có được đọc đúng không
if image is None:
    print("Không thể mở ảnh. Kiểm tra lại đường dẫn.")
else:
    # Biến đổi Fourier 2D
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)  # Dịch chuyển tần số thấp về giữa

    # Tính phổ công suất
    magnitude_spectrum = 20 * np.log(np.abs(fshift))

    # Hiển thị ảnh gốc và phổ công suất
    plt.subplot(121), plt.imshow(image, cmap='gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(magnitude_spectrum, cmap='gray')
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    plt.show()
