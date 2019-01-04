#!/bin/bash

if [ -n "${SINGULARITY_CONTAINER}" ]; then
	cd /DeepSpeech || exit
fi

checkpoint_dir=$(python -c 'from xdg import BaseDirectory as xdg; print(xdg.save_data_path("deepspeech/paldaruo"))')

python -u DeepSpeech.py \
	--train_files /data/paldaruo/train_1.csv \
	--dev_files /data/paldaruo/train_2.csv \
	--test_files /data/paldaruo/test_1.csv \
	--alphabet_config_path /data/paldaruo/alphabet.txt \
	--lm_binary_path /data/paldaruo/lm.binary \
	--lm_trie_path /data/paldaruo/trie \
	--validation_step 10 \
	--train_batch_size 24 \
	--dev_batch_size 48 \
	--test_batch_size 24 \
	--learning_rate 0.0001 \
	--epoch 40 \
	--display_step 5 \
	--dropout_rate 0.20 \
	--default_stddev 0.046875 \
	--checkpoint_dir "$checkpoint_dir" \
	--export_dir /data/output \
	"$@"
