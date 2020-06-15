#!/bin/bash
set -e
set -u
set -o pipefail

source_text_file=''
output_dir=''
test_files=''

alphabet_file_path=/DeepSpeech/bin/bangor_welsh/alphabet.txt
checkpoints_dir=/checkpoints/cy

while getopts ":s:t:o:" opt; do
  case $opt in
    s) 
		    source_text_file=$OPTARG		
        ;;
    t)
        test_files=$OPTARG
        ;;
	  o)
		    output_dir=$OPTARG
		    ;;    
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done
shift "$(($OPTIND -1))"

if [ -z "${source_text_file}" ]; then
	echo "-s source_text_file not set"
    exit 2
fi
if [ -z "$test_files" ]; then
    echo "-t test_files not set (csv file containing speech test set)"
   	exit 2
fi
if [ -z "$output_dir" ]; then
    echo "-o output_dir not set"
   	exit 2
fi


cd ${output_dir}

echo "####################################################################################"
echo "#### Generating binary language model                                           ####"
echo "####################################################################################"
python /DeepSpeech/data/lm/generate_lm.py \
	--input_txt "${source_text_file}" \
  --output_dir . \
  --top_k 50000 \
  --kenlm_bins '/DeepSpeech/native_client/kenlm/build/bin/' \
  --arpa_order 5 \
  --max_arpa_memory '85%' \
  --arpa_prune "0|0|1" \
  --binary_a_bits 255 \
  --binary_q_bits 8 \
  --binary_type 'trie' \
	--discount_fallback


echo "####################################################################################"
echo "#### Generating first language model package                                    ####"
echo "####################################################################################"
python3 /DeepSpeech/data/lm/generate_package.py \
	--alphabet "${alphabet_file_path}" \
	--lm lm.binary \
	--vocab vocab-50000.txt \
  --package kenlm.scorer \
  --default_alpha 0.75 \
	--default_beta 1.85


echo "####################################################################################"
echo "#### Determine optimal alpha and beta parameters                                ####"
echo "####################################################################################"
python /DeepSpeech/lm_optimizer.py \
  --test_files ${test_files} \
  --checkpoint_dir ${checkpoints_dir} \
  --alphabet_config_path ${alphabet_file_path} \
  --scorer kenlm.scorer


echo "####################################################################################"
echo "#### Input required....                                                         ####"
echo "####################################################################################"
read -p "Enter best default alpha: " alpha
read -p "Enter best default beta: " beta


echo "####################################################################################"
echo "#### Generating package with optimal alpha and beta                             ####"
echo "####################################################################################"
python3 /DeepSpeech/data/lm/generate_package.py \
	--alphabet "${alphabet_file_path}" \
	--lm lm.binary \
	--vocab vocab-50000.txt \
  --package kenlm.scorer \
	--default_alpha ${alpha} \
	--default_beta ${beta}

cd -
