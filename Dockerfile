FROM mozilla/deepspeech

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash \
	&& apt-get update && apt-get install -y git-lfs sox \
	&& apt-get clean \
	&& git lfs install \
        && pip install sox wget \
	&& rm -rf /var/lib/apt/lists/* 

ADD bin/* /DeepSpeech/bin/

ENV PATH /DeepSpeech/native_client:/DeepSpeech/native_client/kenlm/build/bin:$PATH

