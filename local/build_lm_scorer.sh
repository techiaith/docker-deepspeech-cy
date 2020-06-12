#!/bin/bash
set -e
set -u
set -o pipefail

source_text_file=''
output_dir=''

alphabet_file_path=/DeepSpeech/bin/bangor_welsh/alphabet.txt

while getopts ":s:o:" opt; do
  case $opt in
    s) 
		    source_text_file=$OPTARG		
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
if [ -z "$output_dir" ]; then
    echo "-o output_dir not set"
   	exit 2
fi

cd ${output_dir}


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


python3 /DeepSpeech/data/lm/generate_package.py \
	--alphabet "${alphabet_file_path}" \
	--lm lm.binary \
	--vocab vocab-50000.txt \
  --package kenlm.scorer \
	--default_alpha 0.931289039105002 \
	--default_beta 1.1834137581510284


cd -
