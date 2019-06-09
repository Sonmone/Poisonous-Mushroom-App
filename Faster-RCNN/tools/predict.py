from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import _init_paths
from model.config import cfg
from model.test import im_detect
from model.nms_wrapper import nms

from utils.timer import Timer
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os, cv2
import argparse

from nets.vgg16 import vgg16
from nets.resnet_v1 import resnetv1

class Predict(object):
    def __init__(self):
	self.CLASSES = ('__background__',  # always index 0
		 'button mushroom', 'death cap', 'earthball mushroom',
		 'ghost fungus', 'haymakers mushroom', 'king oyster mushroom',
		 'pleurotus ostreatus', 'shaggy parasol', 'shimeji mushroom',
		 'slippery jack', 'yellow-staining mushroom', 'green-spored parasol')

	self.final_class = {}
	self.class_box = {}

    def vis_detections(self, im, class_name, dets, thresh=0.5):
	    """Draw detected bounding boxes."""

	    inds = np.where(dets[:, -1] >= thresh)[0]
	    if len(inds) == 0:
		return

	    for i in inds:
		bbox = dets[i, :4]
		score = dets[i, -1]
		if class_name not in self.final_class:
		    self.final_class[class_name] = score
		    self.class_box[class_name] = []
		else:
		    self.final_class[class_name] = max(self.final_class[class_name], score)
		self.class_box[class_name].append([bbox[0].tolist(), bbox[1].tolist(), bbox[2].tolist() - bbox[0].tolist(), bbox[3].tolist() - bbox[1].tolist()])

    def demo(self, sess, net, image_name):
	    """Detect object classes in an image using pre-computed object proposals."""

	    # Load the demo image
	    # im_file = os.path.join(cfg.FLAGS2["data_dir"], 'demo', image_name)
	    im = cv2.imread(image_name)
            im = cv2.transpose(im)
            im = cv2.flip(im,1)
	    # Detect all object classes and regress object bounds
	    timer = Timer()
	    timer.tic()
	    scores, boxes = im_detect(sess, net, im)

	    timer.toc()
	    # Visualize detections for each class
	    CONF_THRESH = 0.1
	    NMS_THRESH = 0.1
	    for cls_ind, cls in enumerate(self.CLASSES[1:]):
		cls_ind += 1  # because we skipped background
		cls_boxes = boxes[:, 4 * cls_ind:4 * (cls_ind + 1)]
		cls_scores = scores[:, cls_ind]
		dets = np.hstack((cls_boxes,
		                  cls_scores[:, np.newaxis])).astype(np.float32)
		keep = nms(dets, NMS_THRESH)
		dets = dets[keep, :]
		self.vis_detections(im, cls, dets, thresh=CONF_THRESH)

    def build_model(self):
	    tfmodel = r'/root/mushroom/tf-faster-rcnn/output/vgg16/voc_2007_trainval/test/vgg16_faster_rcnn_iter_70000.ckpt'
	    demonet = 'vgg16'
	    dataset = 'pascal_voc'
	    if not os.path.isfile(tfmodel + '.meta'):
		# print(tfmodel)
		raise IOError(('{:s} not found.\nDid you download the proper networks from '
		               'our server and place them properly?').format(tfmodel + '.meta'))

	    # set config
	    tfconfig = tf.ConfigProto(allow_soft_placement=True)
	    tfconfig.gpu_options.allow_growth = True

	    # init session
	    self.sess = tf.Session(config=tfconfig)
	    # load network
	    if demonet == 'vgg16':
		self.net = vgg16()
	    # elif demonet == 'res101':
		# net = resnetv1(batch_size=1, num_layers=101)
	    else:
		raise NotImplementedError
	    self.net.create_architecture("TEST", 13,
		                    tag='default', anchor_scales=[8, 16, 32])
	    saver = tf.train.Saver()
	    saver.restore(self.sess, tfmodel)


    def predict(self, img):
	    self.demo(self.sess, self.net, img)
	    #print(final_class.items())
	    #plt.show()
	    if len(self.final_class) > 0:
		    final_class_items = list(self.final_class.items())
		    final_class_items.sort(reverse = True, key = lambda x:x[1])
		    className = str(final_class_items[0][0])
		    classProb = str(final_class_items[0][1])
		    final_cors = self.class_box[final_class_items[0][0]]
		    #print(className, classProb, final_cors)
		    self.final_class.clear()
		    self.class_box.clear()
		    return className, classProb, final_cors
	    else:
		    return None, None, None
