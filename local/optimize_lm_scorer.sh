#!/bin/bash
set -e
set -u
set -o pipefail

lm_dir=''
test_files=''

VOCAB_SIZE=50000

alphabet_file_path=/DeepSpeech/bin/bangor_welsh/alphabet.txt

while getopts ":l:t:" opt; do
  case $opt in
    l) 
		  lm_dir=$OPTARG		
      ;;	  
    t) 
		  test_files=$OPTARG		
		  ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done
shift "$(($OPTIND -1))"

if [ -z "${lm_dir}" ]; then
	echo "-l lm_dir not set"
    exit 2
fi
if [ -z "$test_files" ]; then
    echo "-t test_files not set"
   	exit 2
fi

checkpoint_cy_dir=/checkpoints/cy

cd ${lm_dir}

# Force UTF-8 output
export PYTHONIOENCODING=utf-8	

echo "####################################################################################"
echo "#### Determine optimal alpha and beta parameters                                ####"
echo "####################################################################################"
python /DeepSpeech/lm_optimizer.py \
  --test_files ${test_files} \
  --checkpoint_dir ${checkpoint_cy_dir} \
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
/DeepSpeech/native_client/generate_scorer_package \
	--alphabet "${alphabet_file_path}" \
	--lm lm.binary \
	--vocab vocab-${VOCAB_SIZE}.txt \
  	--package kenlm.scorer \
	--default_alpha ${alpha} \
	--default_beta ${beta}

cd -
