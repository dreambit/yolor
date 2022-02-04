import os
import csv
import math
import cv2


class_names = ["plane", "ship", "storage-tank", "baseball-diamond", "tennis-court", "basketball-court", 
    "ground-track-field", "harbor", "bridge", "large-vehicle", "small-vehicle", "helicopter", "roundabout", 
    "soccer-ball-field", "swimming-pool", "container-crane", "airport", "helipad"]

def get_length(x0, y0, x1, y1):
    x = x1 - x0
    y = y1 - y0
    length = math.sqrt(x*x + y*y)
    return length


#in_dir = "./val_labelTxt/"
#in_dir = "./Val_Task2_gt_non_rotated/"
#img_dir = "../val/images/"

in_dir = "./labelTxt/"
#in_dir = "./Train_Task2_gt_non_rotated/"
img_dir = "../train/images/"

save_angle = True

out_dir = "./out/"

directory = os.fsencode(in_dir)
    
for file in os.listdir(directory):
    file = os.fsdecode(file)
    filename = in_dir + file
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
        with open(out_dir + file, 'w') as f:
            for idx, rows in enumerate(label_file):
                if idx < 2:
                    continue

                x0 = float(rows[0])
                y0 = float(rows[1])

                x1 = float(rows[2])
                y1 = float(rows[3])

                x2 = float(rows[4])
                y2 = float(rows[5])

                x3 = float(rows[6])
                y3 = float(rows[7])

                obj_name = rows[8]
                difficult = rows[9]

                print(f" x0 = {x0}, y0 = {y0}")

                center_x = (x0 + x1 + x2 + x3) / 4
                center_y = (y0 + y1 + y2 + y3) / 4

                # moving center of bbox to the zero
                xm0 = x0 - center_x
                ym0 = y0 - center_y

                xm1 = x1 - center_x
                ym1 = y1 - center_y

                xm2 = x2 - center_x
                ym2 = y2 - center_y

                xm3 = x3 - center_x
                ym3 = y3 - center_y

                # get angle
                bbox_edge_x0 = (xm3 + xm0) / 2
                bbox_edge_y0 = (ym3 + ym0) / 2

                angle = math.atan2(bbox_edge_y0, bbox_edge_x0) / math.pi

                print(f"xy: {x0},{y0} {x1},{y1} {x2},{y2} {x3},{y3}")
                print(f"xym: {xm0},{ym0} {xm1},{ym1} {xm2},{ym2} {xm3},{ym3}")
                print(f" bbox_edge: {bbox_edge_x0},{bbox_edge_y0} angle = {angle}")

                w1 = get_length(x0,y0, x1,y1)
                h1 = get_length(x1,y1, x2,y2)
                w2 = get_length(x2,y2, x3,y3)
                h2 = get_length(x3,y3, x0,y0)

                height = (h1 + h2) / 2
                width = (w1 + w2) / 2

                class_id = class_names.index(obj_name)

                print(f" class_id = {class_id}, center_x = {center_x}, center_y = {center_y}, width = {width}, height = {height}")
            
                #print(f" file = {file}")
                
                center_x = center_x/img_width
                center_y = center_y/img_height

                width = width/img_width
                height = height/img_height

                if width > 1.0 and width < 1.3:
                    width = 0.999

                if height > 1.0 and height < 1.3:
                    height = 0.999


                if width > 1.0 or width < 0.0 or height > 1.0 or height < 0.0:
                    continue

                if center_x > 1.0 or center_x < 0.0 or center_y > 1.0 or center_y < 0.0:
                    continue


                if save_angle:
                    line = (class_id, center_x, center_y, width, height, angle)
                else:
                    line = (class_id, center_x, center_y, width, height)
                 
                f.write(('%g ' * len(line)).rstrip() % line + '\n')


            print("\n")
        continue
    else:
        continue


