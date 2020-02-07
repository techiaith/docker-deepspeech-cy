#!/bin/bash

if [ -n "${SINGULARITY_CONTAINER}" ]; then
	cd /DeepSpeech || exit
fi

checkpoint_dir=$(python -c 'from xdg import BaseDirectory as xdg; print(xdg.save_data_path("deepspeech/cv-train-other_test"))')

export_dir=/export/cv-train-other_test
summary_dir=/keep/transfer/summaries
alphabet_file=/DeepSpeech/bin/bangor_welsh/alphabet.txt
train_files=/data/commonvoice-cy-v4-20191210/deepspeech.train.csv,/data/commonvoice-cy-v4-20191210/deepspeech.other.csv
dev_files=/data/commonvoice-cy-v4-20191210/deepspeech.dev.csv
test_files=/data/commonvoice-cy-v4-20191210/deepspeech.test.csv

rm -rf $checkpoint_dir
rm -rf $export_dir
rm -rf $summary_dir

python3 /DeepSpeech/bin/bangor_welsh/check_alphabets.py -csv "$train_files,$dev_files,$test_files" -a "$alphabet_file"

python -u /DeepSpeech/DeepSpeech.py \
	--train_files  "$train_files" \
	--dev_files "$dev_files" \
	--test_files "$test_files" \
	--alphabet_config_path "$alphabet_file" \
	--lm_binary_path /data/commonvoice-cy/lm.binary \
	--lm_trie_path /data/commonvoice-cy/trie \
	--epochs 20 \
	--drop_source_layers 2 \
	--nofine_tune \
	--source_model_checkpoint_dir /checkpoints/mozilla/deepspeech-0.5.1-checkpoint \
	--train_batch_size 48 \
	--test_batch_size 48 \
	--dev_batch_size 48 \
	--checkpoint_dir "$checkpoint_dir" \
	--summary_dir "$summary_dir" \
	--export_dir "$export_dir" \
	"$@"

