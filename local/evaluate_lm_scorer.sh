#!/bin/bash
set -e
set -u
set -o pipefail

lm_dir=''
test_files=''

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
lm_scorer_path=${lm_dir}/kenlm.scorer

# Force UTF-8 output
export PYTHONIOENCODING=utf-8

set +x
echo "####################################################################################"
echo "#### Evaluate Scorer with previous Welsh checkpoint model														   ###"
echo "####################################################################################"
set -x
python -u evaluate.py \
	--test_files "${test_files}" --test_batch_size 1 \
    --alphabet_config_path "${alphabet_file_path}" \
    --load_checkpoint_dir "${checkpoint_cy_dir}" \
    --scorer_path "${lm_scorer_path}"
	