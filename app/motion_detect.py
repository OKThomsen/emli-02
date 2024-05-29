import sys
import cv2
import numpy as np
import os
import shutil
import time

class cam_class():
    def __init__(self):
        pass
        
    def img_scale(self, img):
        scale_percent = 15 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        img_scaled = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        return img_scaled

    def img_process(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = self.img_scale(img)
        img = cv2.GaussianBlur(img, (21, 21), 0)
        return img
    
    def motion_detect(self, path_img1, path_img2):
        motion = False
        img1 = self.img_process(cv2.imread(path_img1))
        img2 = self.img_process(cv2.imread(path_img2))
        
        # inspired by https://raw.githubusercontent.com/cristianpb/object-detection/master/backend/motion.py
        img_diff = cv2.absdiff(img1, img2)
        #img_prev = img

        # 4. Dilute the image a bit to make differences more seeable; more suitable for contour detection
        kernel = np.ones((5, 5))
        img_diff = cv2.dilate(img_diff, kernel, 1)

        # 5. Only take different areas that are different enough (>20 / 255)
        img_thresh = cv2.threshold(src=img_diff, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[1]

        contours, _ = cv2.findContours(image=img_thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 100:
                # too small: skip!
                continue
            motion = True
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(img=img2, pt1=(x, y), pt2=(x + w, y + h), color=(255, 255, 0), thickness=4)
        
        if motion:
            os.system("./take_photo.sh motion")
            motion = True
            os.remove(path_img1)
            shutil.move(path_img2, path_img1)
        else:
            os.remove(path_img1)
            shutil.move(path_img2, path_img1)

        return motion

def main():
    cam = cam_class()
    while True:
        os.system("./take_tempphoto.sh")
        time.sleep(2)
        
        picture1_path = "./tempphotos/picture1.jpg"
        picture2_path = "./tempphotos/picture2.jpg"

        motion = cam.motion_detect(picture1_path, picture2_path)
        
        if motion:
            print('------------------Motion detected--------------------')
        else:
            print('--------------------No motion------------------------')

if __name__ == "__main__":
    main()
