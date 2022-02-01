import os
import csv
import math
import cv2
import random
import numpy as np

img_dir = "./images/"



class_names = ["plane", "ship", "storage-tank", "baseball-diamond", "tennis-court", "basketball-court", 
    "ground-track-field", "harbor", "bridge", "large-vehicle", "small-vehicle", "helicopter", "roundabout", 
    "soccer-ball-field", "swimming-pool", "container-crane"]


# Refer: https://github.com/ghimiredhikura/Complex-YOLOv3
# bev image coordinates format
def get_corners(x, y, w, l, yaw):
    bev_corners = np.zeros((4, 2), dtype=np.float32)
    cos_yaw = np.cos(yaw)
    sin_yaw = np.sin(yaw)
    # front left
    bev_corners[0, 0] = x - w / 2 * cos_yaw - l / 2 * sin_yaw
    bev_corners[0, 1] = y - w / 2 * sin_yaw + l / 2 * cos_yaw

    # rear left
    bev_corners[1, 0] = x - w / 2 * cos_yaw + l / 2 * sin_yaw
    bev_corners[1, 1] = y - w / 2 * sin_yaw - l / 2 * cos_yaw

    # rear right
    bev_corners[2, 0] = x + w / 2 * cos_yaw + l / 2 * sin_yaw
    bev_corners[2, 1] = y + w / 2 * sin_yaw - l / 2 * cos_yaw

    # front right
    bev_corners[3, 0] = x + w / 2 * cos_yaw - l / 2 * sin_yaw
    bev_corners[3, 1] = y + w / 2 * sin_yaw + l / 2 * cos_yaw

    return bev_corners

    
# draw rotated bounding box (x,y,w,h, angle, color)
def drawRotatedBox(img, x, y, w, l, yaw, color):
    bev_corners = get_corners(x, y, w, l, yaw)
    corners_int = bev_corners.reshape(-1, 1, 2).astype(int)
    cv2.polylines(img, [corners_int], True, color, 2)
    corners_int = bev_corners.reshape(-1, 2)
    cv2.line(img, (corners_int[0, 0], corners_int[0, 1]), (corners_int[3, 0], corners_int[3, 1]), (255, 255, 0), 2)





directory = os.fsencode(img_dir)
    
for file in os.listdir(directory):
    file = os.fsdecode(file)
    filename = img_dir + file
    print(f" filename = {filename}")
    if filename.endswith(".txt"): 
        
        # read image
        pre, ext = os.path.splitext(file)
        img_filename = img_dir + pre + ".png"
        print(f" img_filename = {img_filename}")
        img = cv2.imread(img_filename)
        print(f" img = {img.shape} \n")
        img_width = img.shape[1]
        img_height = img.shape[0]

        label_file = csv.reader(open(filename), delimiter=" ")
        for idx, rows in enumerate(label_file):

            x_center = float(rows[1]) * img_width
            y_center = float(rows[2]) * img_height

            w = float(rows[3]) * img_width
            h = float(rows[4]) * img_height

            angle = float(rows[5])

            color = [random.randint(0, 255) for _ in range(3)]

            drawRotatedBox(img, x_center, y_center, w, h, angle*math.pi, color=color)

        show_img = cv2.resize(img, (1000, 1000)) 

        cv2.imshow("show_img", show_img)
        cv2.waitKey(2000)


        print("\n")
        continue
    else:
        continue


