# thuru_care_server
Thuru Care plant disease identification server by TEAM RGB @IIT
MODULE: (2018) 5COSC009C.2 Software Development Group Project (IIT Sri Lanka)


# Thuru Care Server

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

### Setup

We will be using Python 3 and TensorFlow 1.4

If your tensorflow is not up-to-date use the following command to update.

```sh
$ pip install --upgrade tensorflow
```

### Retrain the model

```sh
$ python3 scripts/retrain.py \
--bottleneck_dir=tf_files/bottlenecks \
--how_many_training_steps 4000 \
--model_dir=tf_files/inception \
--output_graph=tf_files/retrained_graph.pb \
--output_labels=tf_files/retrained_labels.txt \
--image_dir=tf_files/thuru_care_data_set
```

### Run background training

```
$ sudo python scripts/retrain.py \
--bottleneck_dir=tf_files/bottlenecks \
--how_many_training_steps 4000 \
--model_dir=tf_files/inception \
--output_graph=tf_files/retrained_graph.pb \
--output_labels=tf_files/retrained_labels.txt \
--image_dir=tf_files/thuru_care_data_set >> log.txt 2>&1 &
```


## While your computer is training on the new flower dataset let me break down the command and explain what we just did.. 

*Italic*  The whole command can be divided into 4 parts

#### Invoke/Run the retrain.py script.
python scripts/retrain.py

#### Make a new graph file in the tf_files folder(after training is completed).
--output_graph=tf_files/retrained_graph.pb

#### Make a new label file in the tf_files folder (after training is completed).
--output_labels=tf_files/retrained_labels.txt

#### Point towards the flower dataset directory.
--image_dir=tf_files/flower_photos
Note: You can add/change the arguments in the above command

#### Change the model other than Inception-v3 “Mobilenet Models”
--architecture mobilenet_1.0_224

#### Tensorboard
--summaries_dir=tf_files/training_summaries/${write the architecture here}

#### Changing the Bottleneck directory
--bottleneck_dir=tf_files/bottlenecks

#### Changing the Training Steps
--how_many_training_steps=500



#### Test the newly Trained Model

```sh
$ python scripts/label_image.py --image image.png
```

### ////////////////////////////////////  SERVER  //////////////////////////////////// 

### Start Flask server

```sh
$ sudo python app.py >> log.txt 2>&1 &
```

URL : http://www.thurucare.tk:8000
POST request file=image.type
Return JSON out-put as prediction.

