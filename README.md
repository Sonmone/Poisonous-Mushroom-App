# Poisonous-Mushroom-App
The project adopts Faster RCNN to classify the categories of different mushrooms and integrate the model on IOS App.
## Environment
* Ubuntu 18.04
* Python 2.7/3.5
* Tensorflow 1.13.0
* Numpy 1.15.1
* Python-Flask
* Xcode 9.3
## Model - Faster RCNN
### Acknowledgement
The Faster RCNN model is build by TensorFlow, original from https://github.com/endernewton/tf-faster-rcnn, modified by Poisonous-Mushroom-Group.
### Installation
1. Clone the repository
```
https://github.com/Sonmone/Poisonous-Mushroom-App.git
```
2. Configure the Linux Environment
```
Refer to the tutorial in https://github.com/endernewton/tf-faster-rcnn.
```
### Dataset
1. Fetch pre-trained model (VGG-16)
```
mkdir -p data/imagenet_weights
cd data/imagenet_weights
wget -v http://download.tensorflow.org/models/vgg_16_2016_08_28.tar.gz
tar -xzvf vgg_16_2016_08_28.tar.gz
mv vgg_16.ckpt vgg16.ckpt
cd ../..
```
2. Fetch training dataset
* Download dataset from https://drive.google.com/open?id=1amgYMQKcQH-TKGCoQiAZ8PTnU5xZtMoJ
* Move to `data/VOCDevkit2007/VOC2007/`
3. Fetch our trained model
* Download dataset from https://drive.google.com/open?id=11gnkOXU2MWzMQ5G1WEE4KIuCBPF8oKh1
* Move to `output/vgg16/voc_2007_trainval/default/`
### Training
```
./experiments/scripts/train_faster_rcnn.sh 0 pascal_voc vgg16
```
### Predicting
```
./tools/predict.py
```
### Evaluating
```
./experiments/scripts/test_faster_rcnn.sh 0 pascal_voc vgg16
```
## Model - CNN
### Dataset
* Download dataset from https://drive.google.com/open?id=1a1pvL017RQ7L4CS3JE8YRK6jS-71yU7V
* Move to `dataset/`
### Training
```
python train.py
```
### Predicting
```
python predict.py

```
## Mobile application
The iOS Swift Code + API that runs on the server to lisen the request from the iOS APP

### Server API

Running this python code on the remote server
```
    python server.py
```

## Tools
* create_trainval.py - create the training, testing and validation dataset
* Image_Similarity.ipynb - remove duplicated images based on image similarity
* img_classify.py - classify the images into poisonous and edible mushrooms
* name-fix.py - fix the name for xml files
* rotate.py - augment training dataset
