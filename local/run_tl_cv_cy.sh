#!/bin/bash
set -e

###
csv_dir=''
while getopts ":a:" opt; do
  case $opt in
    a) 
		csv_dir=$OPTARG
		;;	      
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

shift "$(($OPTIND -1))"

if [ -z "${csv_dir}" ]; then
    echo "-a csv_dir not set"
    exit 2
fi

###
model_name='bangor-welsh'
model_language='cy-Latn-GB'
model_license='MPL'
model_description='Welsh language acoustic model trained using transfer learning and approximately 90hrs of validated and other Welsh speech data from the Mozilla CommonVoice June 2020 release.'

model_author='techiaith'
model_contact_info='techiaith@bangor.ac.uk'

echo
echo "####################################################################################"
echo " model_name : ${model_name}"
echo " model_language : ${cy-Latn-GB}"
echo " model_license : ${model_license}"
echo " model_description : ${model_description}"
echo " model_author : ${model_author}"
echo " model_contact_info : ${model_contact_info}"
echo " model_version : ${TECHIAITH_RELEASE} "
echo " DeepSpeech Version : ${DEEPSPEECH_RELEASE} "
echo "####################################################################################"
echo

###
train_files=${csv_dir}/validated.clean.csv,${csv_dir}/other.clean.csv
alphabet_cy_file=/DeepSpeech/bin/bangor_welsh/alphabet.txt

checkpoint_dir=/checkpoints
export_dir=/export/${DEEPSPEECH_RELEASE}_${TECHIAITH_RELEASE}


### Force UTF-8 output
export PYTHONIOENCODING=utf-8

checkpoint_en_dir="${checkpoint_dir}/en"
checkpoint_cy_dir="${checkpoint_dir}/cy"

rm -rf ${checkpoint_en_dir}
rm -rf ${checkpoint_cy_dir}
rm -rf ${export_dir}

mkdir -p ${checkpoint_en_dir}
mkdir -p ${checkpoint_cy_dir}
mkdir -p ${export_dir}

cp -r /checkpoints/mozilla/deepspeech-en-checkpoint/ $checkpoint_en_dir

###
echo
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
	--load_checkpoint_dir "${checkpoint_en_dir}"


set +x
echo
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
	--export_model_version "${TECHIAITH_RELEASE}" \
	--export_contact_info "${model_contact_info}" \
	--export_license "${model_license}" \
	--export_language "${model_language}" \
	--export_min_ds_version "${DEEPSPEECH_RELEASE}" \
	--export_max_ds_version "${DEEPSPEECH_RELEASE}" \
	--export_description "${model_description}"

###
/DeepSpeech/native_client/convert_graphdef_memmapped_format \
	--in_graph=${export_dir}/output_graph.pb \
	--out_graph=${export_dir}/output_graph.pbmm


set +x
echo
echo "####################################################################################"
echo "#### Exported acoustic models (.pb/.pbmm files) can be found in ${export_dir} "
echo "####################################################################################"
set -x
