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
	fi
	cd DeepSpeech && docker build --rm -t mozilla/deepspeech .
	docker build --rm -t techiaith/deepspeech .

clean:
	docker rmi techiaith/deepspeech
	#docker rmi mozilla/deepspeech
	
stop:
	docker stop techiaith-deepspeech
	docker rm techiaith-deepspeech

