import os
import pathlib
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from IPython.display import display
from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
from .models import Employee
import re


class Model:
    detection_model = tf.saved_model.load("C:\\Users\\Hussa\\Desktop\\TF2\\Experiment\\inference\\ExportedSavedModel\\saved_model")

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1
# Patch the location of gfile
tf.gfile = tf.io.gfile
# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = "C:\\Users\\Hussa\\Desktop\\TF2\\Experiment\\labelmap.pbtxt"
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=False)
# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
def run_inference_for_single_image(model, image):
    image = np.asarray(image)
    # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
    input_tensor = tf.convert_to_tensor(image)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis,...]
    # Run inference
    model_fn = model.signatures['serving_default']
    output_dict = model_fn(input_tensor)
    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(output_dict.pop('num_detections'))
    output_dict = {key:value[0, :num_detections].numpy() 
    for key,value in output_dict.items()}
    output_dict['num_detections'] = num_detections

    score = output_dict['detection_scores'][0]
    if score < 0.6:
        return "none"   
    
    return category_index[output_dict['detection_classes'][0]]['name']
    
def return_faculty_id(image):
    #return the name of the faculty 
    name = run_inference_for_single_image(Model.detection_model, image)

    #remove any numbers inside name 
    name = re.sub('[123]', '', name)
    name = name.lower()

    #faculties IDs according to the database
    faculties_ids={
        'none' : 0,
        "kasit": 1,
        "medicine": 2,
        "engineering": 3,
        "shareeah": 4,
        "business": 5,
        "law": 7,
        "kitchen": 8,
    }

    print(name)

    return faculties_ids[name]