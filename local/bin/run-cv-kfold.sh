#!/bin/bash

if [ -n "${SINGULARITY_CONTAINER}" ]; then
	cd /DeepSpeech || exit
fi

checkpoint_dir=$(python -c 'from xdg import BaseDirectory as xdg; print(xdg.save_data_path("deepspeech/s4c"))')

rm -rf /export/s4c

python -u DeepSpeech.py \
	--train_files /data/commonvoice-cy/train_1.csv \
	--alphabet_config_path bin/bangor_welsh/alphabet.txt \
	--dev_files /data/commonvoice-cy/train_2.csv \
	--test_files /data/commonvoice-cy/test_1.csv \
	--lm_binary_path /data/commonvoice-cy/lm.binary \
	--lm_trie_path /data/commonvoice-cy/trie \
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


cp bin/bangor_welsh/alphabet.txt /export/cv
cp /data/commonvoice-cy/trie /export/cv
cp /data/commonvoice-cy/lm.binary /export/cv

#convert_graphdef_memmapped_format --in_graph=/export/macsen/output_graph.pb --out_graph=/export/macsen/output_graph.pbmm

