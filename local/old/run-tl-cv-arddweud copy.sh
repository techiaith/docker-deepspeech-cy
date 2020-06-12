#!/bin/bash
set -xe

ldc93s1_dir="/data/smoke_test"
ldc93s1_csv="${ldc93s1_dir}/ldc93s1.csv"

if [ ! -f "${ldc93s1_dir}/ldc93s1.csv" ]; then
    echo "Downloading and preprocessing LDC93S1 example data, saving in ${ldc93s1_dir}."
    python -u bin/import_ldc93s1.py ${ldc93s1_dir}
fi;

alphabet_file=/DeepSpeech/bin/bangor_welsh/alphabet.txt
train_files=/data/commonvoice-cy-v4-20191210/deepspeech.validated.csv,/data/commonvoice-cy-v4-20191210/deepspeech.other.csv
test_files=/data/paldaruo/deepspeech.csv
lm_scorer_path=/data/texts/oscar_commonvoice/kenlm.scorer

checkpoint_dir=$(python -c 'from xdg import BaseDirectory as xdg; print(xdg.save_data_path("deepspeech/cv-tl-arddweud"))')
export_dir=/export/cv-tl-arddweud
summary_dir=/keep/transfer/summaries

rm -rf $checkpoint_dir
rm -rf $export_dir
rm -rf $summary_dir

#python3 /DeepSpeech/bin/bangor_welsh/check_alphabets.py -csv "$train_files,$test_files" -a "$alphabet_file"

echo $checkpoint_dir

# Force UTF-8 output
export PYTHONIOENCODING=utf-8

checkpoint_en_dir="${checkpoint_dir}/en"
checkpoint_cy_dir="${checkpoint_dir}/cy"

mkdir -p ${checkpoint_en_dir}
mkdir -p ${checkpoint_cy_dir}

cp -rv /mozilla/checkpoints/deepspeech-en-checkpoint $checkpoint_en_dir


for LOAD in 'init' 'last' 'auto'; do

	echo "########################################################"
    echo "#### Train ENGLISH model with just --checkpoint_dir ####"
    echo "########################################################"
	python -u /DeepSpeech/DeepSpeech.py \
		--noearly_stop --noshow_progressbar \
		--alphabet_config_path "./data/alphabet.txt" \
		--load_train "$LOAD" \
		--train_files "${ldc93s1_csv}" --train_batch_size 1 \
		--test_files "${ldc93s1_csv}" --test_batch_size 1 \
		--epochs 10 \
		--checkpoint_dir "${checkpoint_en_dir}" \
		--scorer_path ''


	echo "##############################################################################"
    echo "#### Train ENGLISH model with --save_checkpoint_dir --load_checkpoint_dir ####"
    echo "##############################################################################"
	python -u /DeepSpeech/DeepSpeech.py \
		--alphabet_config_path "./data/alphabet.txt" \
		--load_train "$LOAD" \
		--train_files "${ldc93s1_csv}" --train_batch_size 1 \
		--test_files "${ldc93s1_csv}" --test_batch_size 1 \
		--save_checkpoint_dir "${checkpoint_en_dir}" \
		--load_checkpoint_dir "${checkpoint_en_dir}" \
		--epochs 10 \
		--scorer_path ''		


    echo "####################################################################################"
    echo "#### Transfer to WELSH model with --save_checkpoint_dir --load_checkpoint_dir   ####"
    echo "####################################################################################"
    python -u DeepSpeech.py \
        --train_files "${train_files}" --train_batch_size 64 \
        --test_files "${test_files}" --test_batch_size 1 \
        --drop_source_layers 2 \
        --alphabet_config_path "${alphabet_file}" \
        --load_train 'last' \
        --save_checkpoint_dir "${checkpoint_cy_dir}" \
        --load_checkpoint_dir "${checkpoint_en_dir}" \
        --scorer_path '' \
        --epochs 10


	echo "####################################################################################"
    echo "#### Evaluate WELSH model
    echo "####################################################################################"
	python -u evaluate.py \
        --test_files "${test_files}" --test_batch_size 1 \
        --alphabet_config_path "${alphabet_file}" \
        --load_checkpoint_dir "${checkpoint_cy_dir}" \
        --scorer_path "${lm_scorer_path}"

done
