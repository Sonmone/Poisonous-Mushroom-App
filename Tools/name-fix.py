import os
import xml.etree.ElementTree as ET

xmlPath = "Annotations"
for xmlFile in os.listdir(xmlPath):
    filename = os.path.splitext(xmlFile)[0]
    tree = ET.parse(os.path.join(xmlPath, xmlFile))
    root = tree.getroot()
    xml_objects = root.findall("object")
    for xml_object in xml_objects:
        for node in xml_object:
            if node.tag == "name":
                if node.text.lower() == "earthball mushroomw":
                    node.text = "earthball mushroom"
                if node.text.lower() == "king oyster mushroomw":
                    node.text = "king oyster mushroom"
    tree.write(os.path.join(xmlPath, xmlFile))
