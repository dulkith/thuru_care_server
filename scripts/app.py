from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import logging
import random
import time

from flask import Flask, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename

import numpy as np
import tensorflow as tf

#Clint images manage.
UPLOAD_FOLDER = '/home/duka/thuru_care_v3/tensorflask/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph

def read_tensor_from_image_file(file_name, input_height=299, input_width=299,
				input_mean=0, input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(file_reader, channels = 3,
                                       name='png_reader')
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                  name='gif_reader'))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
  else:
    image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                        name='jpeg_reader')
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0);
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

@app.route('/')
def index():
    return '<h1>Welcome to Thuru-Care!</h1>'

@app.route("/", methods=["POST"])
def classify():

    #Get file from POST method.
    file = request.files['file']

    #Save image in server.
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    t = read_tensor_from_image_file(app.config['UPLOAD_FOLDER']+"/"+file.filename,
                                  input_height=input_height,
                                  input_width=input_width,
                                  input_mean=input_mean,
                                  input_std=input_std)
        
    with tf.Session(graph=graph) as sess:
        start = time.time()
        results = sess.run(output_operation.outputs[0],
                      {input_operation.outputs[0]: t})
        end=time.time()
        results = np.squeeze(results)

        top_k = results.argsort()[-5:][::-1]
        labels = load_labels(label_file)

    print('\nEvaluation time (1-image): {:.3f}s\n'.format(end-start))

    for i in top_k:
        print(labels[i], results[i])

    return jsonify(labels,results.tolist())

if __name__ == '__main__':
    # TensorFlow configuration/initialization
    model_file = "retrained_graph.pb"
    label_file = "retrained_labels.txt"
    input_height = 299
    input_width = 299
    input_mean = 128
    input_std = 128
    input_layer = "Mul"
    output_layer = "final_result"

    # Load TensorFlow Graph from disk
    graph = load_graph(model_file)

    # Grab the Input/Output operations
    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name);
    output_operation = graph.get_operation_by_name(output_name);

    # Initialize the Flask Service
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)