#!/bin/bash

if [ -n "${SINGULARITY_CONTAINER}" ]; then
	cd /DeepSpeech || exit
fi

checkpoint_dir=$(python -c 'from xdg import BaseDirectory as xdg; print(xdg.save_data_path("deepspeech/gwion-tl-cv-lleisiwr"))')
export_dir=/export/gwion-tl-cv-lleisiwr
summary_dir=/keep/transfer/summaries

rm -rf $checkpoint_dir
rm -rf $export_dir
rm -rf $summary_dir

python -u /DeepSpeech/DeepSpeech.py \
	--train_files  /data/commonvoice-cy/deepspeech.csv,/data/corpws_lleisiwr/corpws_gwion/train_1.csv \
	--test_files /data/corpws_lleisiwr/corpws_gwion/test_1.csv \
	--alphabet_config_path /DeepSpeech/bin/bangor_welsh/alphabet.txt \
	--lm_binary_path /data/corpws_lleisiwr/corpws_gwion/lm.binary \
	--lm_trie_path /data/corpws_lleisiwr/corpws_gwion/trie \
        --source_model_checkpoint_dir /checkpoints/mozilla/deepspeech-0.5.1-checkpoint \
	--nofine_tune \
	--epochs 20 \
	--drop_source_layers 2 \
	--train_batch_size 48 \
	--test_batch_size 48 \
	--dev_batch_size 48 \
	--checkpoint_dir "$checkpoint_dir" \
	--summary_dir "$summary_dir" \
	--export_dir "$export_dir" \
	"$@"

