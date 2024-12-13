import cv2
import numpy as np
import os

def sharpen_img(image):
    kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])
    image_sharp = image.copy()

    image_sharp = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
    return image_sharp

def high_pass_filter(image):
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    high_pass = cv2.addWeighted(image, 1.5, blurred, -0.5, 0)
    return high_pass

def denoise_image(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 3, 3, 3, 21)


def unsharp_mask(image, sigma=1.0, strength=1.5):
    blurred = cv2.GaussianBlur(image, (0, 0), sigma)
    sharpened = cv2.addWeighted(image, 1 + strength, blurred, -strength, 0)
    
    return sharpened


def adaptive_histogram_equalization(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    
    enhanced_image = cv2.cvtColor(limg, cv2.COLOR_Lab2BGR)
    
    return enhanced_image

def process_image(image):
    denoised = denoise_image(image)
    contrast_enhanced = adaptive_histogram_equalization(denoised)
    sharpened = unsharp_mask(contrast_enhanced)
    
    return sharpened


def unwrap_image(video_path, img_path, show):

    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    W, H = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    column_range = 7

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    output_width = frame_count
    output_image = np.zeros((int(H), (column_range-1)*(int(output_width)), 3), dtype=np.uint8)

    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    # out = cv2.VideoWriter(r'C:\Users\Shirshak\Desktop\Flipkart Grid\Videos\output_video_w.mp4', 
    #                     cv2.VideoWriter_fourcc(*'mp4v'), 
    #                     60, 
    #                     (int(W), int(H)))

    print(f"Width:{W}, Height:{H}")
    print(f"Frame Rate:{frame_rate}")
    print(f"Frame Count:{frame_count}")
    
    kernel = np.ones((3,3), np.uint8)
    i=0

    overlap = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break  

        middle_col_start = int(W // 2) - column_range // 2
        middle_col_end = int(W // 2) + column_range // 2
        middle_cols = frame[:, middle_col_start:middle_col_end]

        current_frame_end = (column_range-1)*(frame_count  - i)
        current_frame_start = (column_range-1)*(frame_count  - (i+1))
        if current_frame_start>0:

            output_image[:, current_frame_start-overlap:current_frame_end-overlap] = middle_cols
        i+=1
        if show==True:
            cv2.imshow("Product", frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()

    print('Product Unwrapping complete')



    # output_image = sharpen_img(output_image)
    # output_image = adaptive_histogram_equalization(output_image)

    # output_image_show = cv2.resize(output_image, (int(output_image.shape[1]//8), int(output_image.shape[0]//8)))
    print(f"Output Shape:{output_image.shape}")
    cv2.imwrite(img_path, output_image)
    print("Image Saved")
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
