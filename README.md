# Poisonous-Mushroom-App
The project adopts Faster RCNN to classify the categories of different mushrooms and integrate the model on IOS App.
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
* Move to `data/VOCDevkit2007/VOC2007`
