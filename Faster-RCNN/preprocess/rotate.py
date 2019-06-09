import os
from PIL import Image
import xml.etree.ElementTree as ET

angles = [Image.ROTATE_90, Image.ROTATE_270]
base_num = 8981
for img in os.listdir(r"./JPEGImages"):
    im = Image.open("./JPEGImages/" + img)
    im = im.convert('RGB')
    img_name = img[:6]
    for i in range(len(angles)):
        xml_name = "./Annotations/" + img_name + ".xml"
        tree = ET.parse(xml_name)
        root = tree.getroot()
        new_im_namepre = str(int(img_name) + i + base_num).zfill(6)
        new_im = im.transpose(angles[i])
        new_im_name = new_im_namepre + ".jpg"
        new_im.save("./JPEGImages/" + new_im_name)
        xml_filename = root.find("filename")
        xml_filename.text = new_im_namepre + ".jpg"
        xml_path = root.find("path")
        xml_path_text = xml_path.text
        xml_path.text = xml_path_text.replace(img_name + ".jpg", new_im_namepre + ".jpg")
        xml_size = root.find("size")
        width = 0
        height = 0
        if angles[i] == Image.ROTATE_90 or angles[i] == Image.ROTATE_270:
            for node in xml_size:
                if node.tag == "width":
                    width = node.text
                if node.tag == "height":
                    height = node.text
                    break
            for node in xml_size:
                if node.tag == "width":
                    node.text = height
                if node.tag == "height":
                    node.text = width
                    break
        xml_objects = root.findall("object")
        for xml_object in xml_objects:
            xmin_rotated = 0
            xmax_rotated = 0
            ymin_rotated = 0
            ymax_rotated = 0
            for node in xml_object:
                if node.tag == "bndbox":
                    for coor in node:
                        if coor.tag == "xmin":
                            xmin = coor.text
                        elif coor.tag == "ymin":
                            ymin = coor.text
                        elif coor.tag == "xmax":
                            xmax = coor.text
                        else:
                            ymax = coor.text
            x_len = int(xmax) - int(xmin)
            y_len = int(ymax) - int(ymin)
            if angles[i] == Image.ROTATE_90:
                xmin_rotated = ymin
                xmax_rotated = ymax
                ymin_rotated = str(int(width) - int(xmax))
                ymax_rotated = str(int(width) - int(xmin))
                # print(xmin_rotated, ymin_rotated,xmax_rotated,ymax_rotated)
            elif angles[i] == Image.ROTATE_270:
                ymin_rotated = xmin
                ymax_rotated = str(int(ymin_rotated) + int(x_len))
                xmax_rotated = str(int(height) - int(ymin))
                xmin_rotated = str(int(height) - int(ymax))
            for node in xml_object:
                if node.tag == "bndbox":
                    for coor in node:
                        if coor.tag == "xmin":
                            coor.text = xmin_rotated
                        elif coor.tag == "ymin":
                            coor.text = ymin_rotated
                        elif coor.tag == "xmax":
                            coor.text = xmax_rotated
                        else:
                            coor.text = ymax_rotated


        tree.write("./Annotations/" + new_im_namepre + ".xml")
    base_num += 1
