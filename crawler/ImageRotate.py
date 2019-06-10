from PIL import Image
import os
from tqdm import tqdm
import sys


#parse all of images of each single category



#parse the directory that contains all categories of mushroom
def readDirectory(filePath): 
    count = 0
    categories = os.listdir(filePath)
    try:
        os.mkdir('./dataset(test)')
    except:
        pass
    for cate in categories:
        count = rotateImages(filePath, cate, count)


def rotateImages(filePath, imageType, count):
    fail = 0
    try:
        store_folder_path = './dataset(test)' + '/' + imageType
        os.mkdir(store_folder_path)
    except:
        pass
    try:
        directory_path = filePath + '/' + imageType
        lists = os.listdir(directory_path)
        print(imageType, '-- start')
        failiure_logo = open(store_folder_path + '/' + imageType+'.txt','w')
        for list in tqdm(lists):
            image_path = directory_path + '/' + list
            try:
                image = Image.open(image_path)
                for angle in [0,90,180,270]:
                    count = count + 1
                    rotate = image.rotate(angle)
                    order = str(format(count, '06d'))
                    save_path = store_folder_path+ '/' + order + '.jpg'
                    rotate.save(save_path)
            except:
                failiure_logo.write(image_path)
                failiure_logo.write('\n')
                fail += 1
        print(imageType, '-- finished')
        if fail == 0:
            failiure_logo.write('all success!')
        else:
            failiure_logo.write('total:' + str(fail))
        failiure_logo.close()
        return count
    except:
        print('Connot find ', directory_path)



# if __name__ == "__main__":
#     readDirectory(sys.argv[1])
os.mkdir('./dataset(test)')
rotateImages('./image', 'Death Cap', 0)

