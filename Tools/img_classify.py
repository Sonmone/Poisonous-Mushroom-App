import os
from PIL import Image

root_dir = os.walk("G:\\Computing_Project\\data\\dataset")
save_dir = "G:\\Computing_Project\\data\\train\\"
poisonous = ["Death Cap","ghost fungus","green-spored parasol","Haymakers mushroom","yellow-staining mushroom","earthball mushroom"]
edible = ["Agaricus augustus","button mushroom","hericium erinaceus","king oyster mushroom","Pleurotus ostreatus","Shaggy Parasol","shimeji mushroom","slippery Jack","The Saffron Milk Cap","Wood Blewit"]
poisonous_num = 0
edible_num = 0
for path, dir_list, file_list in root_dir:
    for folder_name in dir_list:
        img_foler_dir = os.path.join(path, folder_name)
        for img in os.listdir(img_foler_dir):
            img_path = os.path.join(path, folder_name, img)
            try:
                im = Image.open(img_path)
                im = im.convert('RGB')
                if folder_name in poisonous:
                    new_im_name = "poisonous." + str(poisonous_num) + ".jpg"
                    poisonous_num += 1
                else:
                    new_im_name = "edible." + str(edible_num) + ".jpg"
                    edible_num += 1
                im.save(save_dir + new_im_name)
            except(OSError, NameError):
                print(NameError)
