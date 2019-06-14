FROM mozilla/deepspeech

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash \
	&& apt-get update && apt-get install -y git-lfs lame sox vim zip file \
						unzip python3 python3-pip python3-dev  \
						libffi-dev libssl-dev libxml2-dev \
						libxslt1-dev libjpeg8-dev zlib1g-dev \
	&& apt-get clean \
	&& git lfs install \
        && pip3 install sox wget sklearn pandas virtualenv requests \
	&& rm -rf /var/lib/apt/lists/* 

WORKDIR /DeepSpeech

ADD local/bin/* /DeepSpeech/bin/

ENV PATH /DeepSpeech/native_client:/DeepSpeech/native_client/kenlm/build/bin:$PATH

