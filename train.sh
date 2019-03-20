# Run tensorflow flask serving
python3 scripts/retrain.py \
--bottleneck_dir=tf_files/bottlenecks \
--how_many_training_steps 4000 \
--model_dir=tf_files/inception \
--output_graph=tf_files/retrained_graph.pb \
--output_labels=tf_files/retrained_labels.txt \
--image_dir=tf_files/thuru_care_data_set

# Run tensorflow flask serving.
$sudo python app1c.py >> log.txt 2>&1 &