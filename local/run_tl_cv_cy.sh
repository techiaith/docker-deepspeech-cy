#!/bin/bash
set -xe

###
model_name='bangor'
model_language='cy-Latn-GB'
model_license='CC-BY-4.0'
model_description='Welsh language acoustic model trained using transfer learning and approximately 77hrs of Welsh speech data from the Mozilla CommonVoice December 2019 release.'

model_author='techiaith'
model_contact_info='techiaith@bangor.ac.uk'

model_version='20.06'
deepspeech_version='0.7.3'


###
train_files=/data/commonvoice-cy-v4-20191210/deepspeech.validated.csv,/data/commonvoice-cy-v4-20191210/deepspeech.other.csv
alphabet_cy_file=/DeepSpeech/bin/bangor_welsh/alphabet.txt

checkpoint_dir=/checkpoints
export_dir=/export/cv-tl-cy


### Force UTF-8 output
export PYTHONIOENCODING=utf-8

checkpoint_en_dir="${checkpoint_dir}/en"
checkpoint_cy_dir="${checkpoint_dir}/cy"

rm -rf ${checkpoint_en_dir}
rm -rf ${checkpoint_cy_dir}

mkdir -p ${checkpoint_en_dir}
mkdir -p ${checkpoint_cy_dir}

cp -rv /checkpoints/mozilla/deepspeech-en-checkpoint/ $checkpoint_en_dir


###
set +x
echo "####################################################################################"
echo "#### Transfer to WELSH model with --save_checkpoint_dir --load_checkpoint_dir   ####"
echo "####################################################################################"
set -x
python -u DeepSpeech.py \
	--train_files "${train_files}" --train_batch_size 64 \
	--drop_source_layers 2 \
	--epochs 10 \
	--alphabet_config_path "${alphabet_cy_file}" \
	--save_checkpoint_dir "${checkpoint_cy_dir}" \
	--checkpoint_dir "${checkpoint_cy_dir}" \
	--load_checkpoint_dir "${checkpoint_en_dir}"


set +x
echo "####################################################################################"
echo "#### Export new Welsh checkpoint to frozen model								  ####"
echo "####################################################################################"
set -x
python -u DeepSpeech.py \
	--train_files "${train_files}" --train_batch_size 64 \
	--epochs 1 \
	--alphabet_config_path "${alphabet_cy_file}" \
	--save_checkpoint_dir "${checkpoint_cy_dir}" \
	--load_checkpoint_dir "${checkpoint_cy_dir}" \
	--remove_export \
	--export_dir "${export_dir}" \
	--export_author_id "${model_author}" \
	--export_model_name "${model_name}" \
	--export_model_version "${model_version}" \
	--export_contact_info "${model_contact_info}" \
	--export_license "${model_license}" \
	--export_language "${model_language}" \
	--export_min_ds_version "${deepspeech_version}" \
	--export_max_ds_version "${deepspeech_version}" \
	--export_description "${model_description}"
