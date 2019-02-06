# thuru_care_server
Thuru Care plant disease identification server by TEAM RGB @IIT
MODULE: (2018) 5COSC009C.2 Software Development Group Project (IIT Sri Lanka)


Retrain the model:
python scripts/retrain.py --output_graph=tf_files/retrained_graph.pb --output_labels=tf_files/retrained_labels.txt --image_dir=tf_files/flower_photos

Test the newly Trained Model:
python scripts/label_image.py --image New-Ford-Mustang.1910x1000.jpg