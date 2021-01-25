#!/bin/bash
set -e
set -u
set -o pipefail

testset_dir=''
scorer_path=''

alphabet_file_path=/DeepSpeech/bin/bangor_welsh/alphabet.txt
checkpoint_cy_dir=/checkpoints/cy

while getopts ":t:s:" opt; do
  case $opt in    
    t)
        testset_dir=$OPTARG
        ;;
	  s)
		    scorer_path=$OPTARG
		    ;;    
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done
shift "$(($OPTIND -1))"

if [ -z "$testset_dir" ]; then
    echo "-t testset_dir not set (csv file containing speech test set)"
   	exit 2
fi
if [ -z "$scorer_path" ]; then
    echo "-s scorer_path not set"
   	exit 2
fi


set +x
echo "####################################################################################"
echo "#### evaluating with transcriber testset                											   ###"
echo "####################################################################################"
set -x

python -u /DeepSpeech/evaluate.py \
	--test_files "${testset_dir}/data/trawsgrifio/OpiwHxPPqRI/deepspeech.csv" \
  --test_batch_size 1 \
	--alphabet_config_path "${alphabet_file_path}" \
	--load_checkpoint_dir "${checkpoint_cy_dir}" \
	--scorer_path "${scorer_path}"
