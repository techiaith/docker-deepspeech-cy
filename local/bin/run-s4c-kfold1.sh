#!/bin/bash

if [ -n "${SINGULARITY_CONTAINER}" ]; then
	cd /DeepSpeech || exit
fi

checkpoint_dir=$(python -c 'from xdg import BaseDirectory as xdg; print(xdg.save_data_path("deepspeech/s4c"))')

rm -rf /export/s4c

python -u DeepSpeech.py \
	--train_files /data/commonvoice-cy/deepspeech.csv \
	--alphabet_config_path /data/corpws_s4c/alphabet.txt \
	--dev_files /data/corpws_s4c/train_1.csv \
	--test_files /data/corpws_s4c/test_1.csv \
	--lm_binary_path /data/corpws_s4c/lm.binary \
	--lm_trie_path /data/corpws_s4c/trie \
	--validation_step 10 \
	--train_batch_size 24 \
	--dev_batch_size 48 \
	--test_batch_size 24 \
	--learning_rate 0.0001 \
	--epoch 1000 \
	--display_step 5 \
	--dropout_rate 0.20 \
	--default_stddev 0.046875 \
	--checkpoint_dir "$checkpoint_dir" \
	--export_dir /export/s4c \
	"$@"


cp /data/commonvoice-cy/alphabet.txt /export/s4c
cp /data/testsets/macsen/trie /export/s4c
cp /data/testsets/macsen/lm.binary /export/s4c

#convert_graphdef_memmapped_format --in_graph=/export/macsen/output_graph.pb --out_graph=/export/macsen/output_graph.pbmm

