#!/bin/bash

if [ -n "${SINGULARITY_CONTAINER}" ]; then
	cd /DeepSpeech || exit
fi

checkpoint_dir=$(python -c 'from xdg import BaseDirectory as xdg; print(xdg.save_data_path("deepspeech/s4c"))')

rm -rf /export/s4c

python -u DeepSpeech.py \
	--train_files /data/corpws_s4c/train_1.csv \
	--alphabet_config_path bin/bangor_welsh/alphabet.txt \
	--test_files /data/corpws_s4c/test_1.csv \
	--lm_binary_path /data/corpws_s4c/lm.binary \
	--lm_trie_path /data/corpws_s4c/trie \
	--train_batch_size 24 \
	--test_batch_size 24 \
	--epochs 20 \
	--checkpoint_dir "$checkpoint_dir" \
	--export_dir /export/s4c \
	"$@"


cp bin/bangor_welsh/alphabet.txt /export/s4c
cp /data/corpws_s4c/trie /export/s4c
cp /data/corpws_s4c/lm.binary /export/s4c

#convert_graphdef_memmapped_format --in_graph=/export/macsen/output_graph.pb --out_graph=/export/macsen/output_graph.pbmm

