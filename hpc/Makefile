SHELL:=/bin/bash

# Required when not using the maximum number of cores on a node
SCW_TPN_OVERRIDE:=1
export SCW_TPN_OVERRIDE

default: build

run:
	# Request system resources and submit a job to the cluster
	./scw run-macsen.sh

build:
	# Build the singulairty image
	module load singularity/2.5.2; \
	singularity build techiaith_deepspeech.simg docker://techiaith/deepspeech:latest

	# Set file permissions
	chmod +x scw

clean:
	# Remove the singularity image
	rm techiaith_deepspeech.simg

	# Clear logs
	rm *err*
	rm *out*
	rm *log*

update:
	# Pull in repo updates
	git pull
