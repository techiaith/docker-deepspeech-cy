#!/bin/bash

if [ -n "${SINGULARITY_CONTAINER}" ]; then
	cd /DeepSpeech || exit
fi

checkpoint_dir=$(python -c 'from xdg import BaseDirectory as xdg; print(xdg.save_data_path("deepspeech/cv-validated-other-paldaruo-plus-mozilla"))')

export_dir=/export/cv-validated-other-mozilla
summary_dir=/keep/transfer/summaries
alphabet_file=/DeepSpeech/bin/bangor_welsh/alphabet_macsen.txt
train_files=/data/commonvoice-cy-v4-20191210/deepspeech.validated.csv
#train_files=/data/commonvoice-cy-v3-20190624/deepspeech.validated.csv,/data/commonvoice-cy-v3-20190624/deepspeech.other.csv

#train_files=/data/commonvoice-cy-v3-20190624/deepspeech.train.csv
#train_files=/data/commonvoice-cy-v3-20190624/deepspeech.validated.csv,/data/commonvoice-cy-v3-20190624/deepspeech.other.csv

#dev_files=/data/commonvoice-cy-v4-20191210/deepspeech.dev.csv
echo "kfold $1"
dev_files="/data/macsen/train_$1.csv"

#test_files=/data/commonvoice-cy-v4-20191210/deepspeech.test.csv
#test_files=/data/paldaruo/deepspeech.csv
test_files="/data/macsen/test_$1.csv"

lm_binary_path=/data/macsen/lm.binary
lm_trie_path=/data/macsen/trie

#lm_binary_path=/data/texts/oscar_macsen/lm.binary
#lm_trie_path=/data/texts/oscar_macsen/trie
#lm_binary_path=/data/texts/oscar/lm.binary
#lm_trie_path=/data/texts/oscar/trie

rm -rf $checkpoint_dir
rm -rf $export_dir
rm -rf $summary_dir


#python3 /DeepSpeech/bin/bangor_welsh/check_alphabets.py -csv "$train_files,$test_files" -a "$alphabet_file"

python -u /DeepSpeech/DeepSpeech.py \
	--train_files  "$train_files" \
	--dev_files "$dev_files" \
	--test_files "$test_files" \
	--alphabet_config_path "$alphabet_file" \
	--lm_binary_path "$lm_binary_path" \
	--lm_trie_path "$lm_trie_path" \
	--epochs 20 \
	--train_batch_size 64 \
	--dev_batch_size 48 \
	--test_batch_size 12 \
	--checkpoint_dir "$checkpoint_dir" \
	--summary_dir "$summary_dir" \
	--export_dir "$export_dir" \
	"$@"

