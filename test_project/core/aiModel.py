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
from .models import *
import re

MIN_DETECTION_SCORE = 0.6

#this class Model loads the trained model and the neccassary id and names from database
# into main memory at program initialization 
class Model:
    detection_model = tf.saved_model.load("C:\\Users\\Hussa\\Desktop\\TF2\\Experiment\\inference\\ExportedSavedModel\\saved_model")

    getId = {}
    #map each original name from database to ID
    for id_and_name in Faculty.objects.values('id', 'name'):
        getId[id_and_name['name']] = id_and_name['id'] 

    #map names coming from model to their ids using the map "getId"
    faculties_ids={
        'none' : 0,
        "kasit": getId['King Abdulla II School For Information Technology'],
        "medicine": getId['School of Medicine'],
        "engineering": getId['School of Engineering'],
        "shareeah": getId['School of Sharia'],
        "business": getId['School of Business'],
        "law": getId['School of Law'],
        "kitchen": getId['Community Restaurant'],
        "educational" : getId['School of Educational Sciences'],
        'nursing': getId['School of Nursing'],
        'pharamcy': getId['School of Pharmacy'],
        'dentistry' : getId['School of Dentistry'],
        'rehabilitation' : getId['School of Rehabilitation Sciences'],
        'arts - design' : getId['School of Arts and Design'],
        'languages' : getId['School of Foreign Languages'],
        'arts' : getId['School of Arts'],
        'science' : getId['School of Science'],
        }

    print(faculties_ids)

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
    print(score)
    if score < MIN_DETECTION_SCORE:
        return "none"   
    
    return category_index[output_dict['detection_classes'][0]]['name']
    
def return_faculty_id(image):
    #return the name of the faculty 
    name = run_inference_for_single_image(Model.detection_model, image)

    #remove any numbers inside name 
    name = re.sub('[123]', '', name)
    name = name.lower()
    
    return Model.faculties_ids[name]
    