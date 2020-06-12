#!/bin/bash

if [ -n "${SINGULARITY_CONTAINER}" ]; then
	cd /DeepSpeech || exit
fi

checkpoint_dir=$(python -c 'from xdg import BaseDirectory as xdg; print(xdg.save_data_path("deepspeech/macsen"))')

python -u DeepSpeech.py \
	--train_files /data/commonvoice-cy/deepspeech.csv,/data/macsen/train_1.csv \
	--alphabet_config_path /data/alphabet.txt \
	--dev_files /data/macsen/test_2.csv \
	--test_files /data/macsen/test_2.csv \
	--lm_binary_path /data/macsen/lm.binary \
	--lm_trie_path /data/macsen/trie \
	--beam_width 500 \
	--lm_alpha 0.75 \
	--lm_beta 1.85 \
	--train_batch_size 24 \
	--dev_batch_size 24 \
	--test_batch_size 24 \
	--epochs 75 \
	--augmentation_pitch_and_tempo_scaling \
	--augmentation_freq_and_time_masking \
	--checkpoint_dir "$checkpoint_dir" \
	--export_dir /export/macsen \
	--remove_export True \
	--export_language cy \
	"$@"


cp /data/alphabet.txt /export/macsen
cp /data/macsen/trie /export/macsen
cp /data/macsen/lm.binary /export/macsen

#convert_graphdef_memmapped_format --in_graph=/export/macsen/output_graph.pb --out_graph=/export/macsen/output_graph.pbmm

