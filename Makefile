default: build
DEEPSPEECH_RELEASE := 0.6.1

run: 
	docker run --gpus all --name techiaith-deepspeech-${USER} -it \
		-v ${PWD}/data/:/data \
                -v $(PWD)/../Corpws-S4C/data/corpws/:/data/corpws_s4c/audio/ \
                -v ${PWD}/checkpoints/:/checkpoints \
		-v ${PWD}/export/:/export \
		-v ${PWD}/tmp/:/tmp \
		-v ${PWD}/homedir/:/root \
		-v ${PWD}/local/bin:/DeepSpeech/bin/bangor_welsh \
		techiaith/deepspeech bash
	
build:
	if [ ! -d "DeepSpeech" ]; then \
	    git clone --branch v$(DEEPSPEECH_RELEASE) https://github.com/mozilla/DeepSpeech.git; \
            cd DeepSpeech && docker build --rm -t mozilla/deepspeech .; \
	fi
	if [ ! -d "checkpoints/mozilla" ]; then \
	    mkdir -p checkpoints/mozilla; \
	    cd checkpoints/mozilla && \
		wget https://github.com/mozilla/DeepSpeech/releases/download/v$(DEEPSPEECH_RELEASE)/deepspeech-$(DEEPSPEECH_RELEASE)-checkpoint.tar.gz && \
		tar xvfz deepspeech-$(DEEPSPEECH_RELEASE)-checkpoint.tar.gz;\
	fi
	docker build --rm -t techiaith/deepspeech .

clean:
	-docker rmi techiaith/deepspeech
	-docker rmi mozilla/deepspeech
	-docker rmi nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04
	sudo rm -rf DeepSpeech
	sudo rm -rf homedir
	
stop:
	-docker stop techiaith-deepspeech-${USER}
	-docker rm techiaith-deepspeech-${USER}

