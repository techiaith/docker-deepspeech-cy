default: build

run: 
	nvidia-docker run --name techiaith-deepspeech -it \
		-v ${PWD}/data/:/data \
		-v ${PWD}/tmp/:/tmp \
		-v ${PWD}/homedir/:/root \
		techiaith/deepspeech bash
	
build:
	if [ ! -d "DeepSpeech" ]; then \
	    git clone https://github.com/mozilla/DeepSpeech.git; \
            cd DeepSpeech && docker build --rm -t mozilla/deepspeech .; \
	fi
	if [ ! -d "CorporaCreator" ]; then \
	    git clone https://github.com/mozilla/CorporaCreator.git; \
	fi
	docker build --rm -t techiaith/deepspeech .

clean:
	docker rmi techiaith/deepspeech
	docker rmi mozilla/deepspeech
	docker rmi nvidia/cuda:9.0-cudnn7-devel-ubuntu16.04
	sudo rm -rf DeepSpeech
	sudo rm -rf homedir
	
stop:
	docker stop techiaith-deepspeech
	docker rm techiaith-deepspeech

