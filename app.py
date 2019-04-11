from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import logging
import random
import time

from flask import Flask, jsonify, request, redirect, url_for
from flask_restplus import Api, Resource
from werkzeug.utils import secure_filename

from werkzeug.datastructures import FileStorage

import numpy as np
import tensorflow as tf
import json

#Clint images manage.
UPLOAD_FOLDER = '/home/duka/thuru_care_v3/tensorflask/uploads'


app = Flask(__name__)
api = Api(app=app,
          version='1.0',
          title='Thuru-Care REST Api',
          description='RESTful API wrapper for Thuru-Care client')

# create dedicated namespace for GAN client
ns_conf = api.namespace('api', description='Operations for GAN client')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Flask-RestPlus specific parser for image uploading
UPLOAD_KEY = 'image'
UPLOAD_LOCATION = 'files'
upload_parser = api.parser()
upload_parser.add_argument(UPLOAD_KEY,
                           location=UPLOAD_LOCATION,
                           type=FileStorage,
                           required=True)

@ns_conf.route('/prediction')
class GanPrediction(Resource):
    @ns_conf.doc(description='Predict the house number on the image using GAN model. ' +
            'Return 3 most probable digits with their probabilities',
            responses={
                200: "Success",
                400: "Bad request",
                500: "Internal server error"
                })
    @ns_conf.expect(upload_parser)
    def post(self):
        try:
            image_file = request.files[UPLOAD_KEY]
            #image = io.BytesIO(image_file.read())
        except Exception as inst:
            return {'message': 'something wrong with incoming request. ' +
                               'Original message: {}'.format(inst)}, 400

        try:
            results_json = classify(image_file)
            return {'prediction_result': results_json}, 200

        except Exception as inst:
            return {'message': 'internal error: {}'.format(inst)}, 500









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
def classify(file = None):

    #Get file from POST method.
    if(file is None):
      file = request.files[UPLOAD_KEY]

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

    #return jsonify(labels,results.tolist())

    dictionary = dict(zip(labels, results))
    
    return jsonify(dictionary)
    #return jsonify(dictionary)

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