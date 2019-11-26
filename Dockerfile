FROM mozilla/deepspeech

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash \
	&& apt-get update && apt-get install -y git-lfs lame sox vim zip file \
						unzip python3 python3-pip python3-dev  \
						libffi-dev libssl-dev libxml2-dev \
						libxslt1-dev libjpeg8-dev zlib1g-dev dos2unix\
	&& apt-get clean \
	&& git lfs install \
        && pip3 install sox wget sklearn pandas python_speech_features virtualenv requests jiwer \
	&& rm -rf /var/lib/apt/lists/* 

WORKDIR /DeepSpeech

#RUN python3 util/taskcluster.py --source tensorflow --artifact convert_graphdef_memmapped_format --target native_client \
#	&& chmod +x native_client/convert_graphdef_memmapped_format

#ADD local/bin/* /DeepSpeech/bin/bangor_welsh/
COPY alphabet.txt /DeepSpeech/bin/bangor_welsh/

ENV PATH /DeepSpeech/native_client:/DeepSpeech/native_client/kenlm/build/bin:$PATH

