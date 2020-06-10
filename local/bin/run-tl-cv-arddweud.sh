#!/bin/bash

if [ -n "${SINGULARITY_CONTAINER}" ]; then
	cd /DeepSpeech || exit
fi

checkpoint_dir=$(python -c 'from xdg import BaseDirectory as xdg; print(xdg.save_data_path("deepspeech/cv-tl-arddweud"))')

export_dir=/export/cv-tl-arddweud
summary_dir=/keep/transfer/summaries

alphabet_file=/DeepSpeech/bin/bangor_welsh/alphabet.txt

train_files=/data/commonvoice-cy-v4-20191210/deepspeech.validated.csv,/data/commonvoice-cy-v4-20191210/deepspeech.other.csv

test_files=/data/paldaruo/deepspeech.csv

lm_scorer_path=/data/texts/oscar_commonvoice/kenlm.scorer

rm -rf $checkpoint_dir
rm -rf $export_dir
rm -rf $summary_dir

#python3 /DeepSpeech/bin/bangor_welsh/check_alphabets.py -csv "$train_files,$test_files" -a "$alphabet_file"

python -u /DeepSpeech/DeepSpeech.py \
	--train_files  "$train_files" \
	--test_files "$test_files" \
	--alphabet_config_path "$alphabet_file" \
	--scorer_path "$lm_scorer_path"
	--epochs 10 \
	--drop_source_layers 2 \
	--nofine_tune \
	--source_model_checkpoint_dir /checkpoints/mozilla/deepspeech-0.5.1-checkpoint \
	--train_batch_size 48 \
	--test_batch_size 12 \
	--checkpoint_dir "$checkpoint_dir" \
	--summary_dir "$summary_dir" \
	--export_dir "$export_dir" \
	"$@"

#cp $alphabet_file $export_dir
#cp $lm_binary_path $export_dir
#cp $lm_trie_path $export_dir

