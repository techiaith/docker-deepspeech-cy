ARG BRANCH
FROM mozilla/deepspeech:$BRANCH

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash \
	&& apt-get update && apt-get install -y git-lfs lame sox vim zip file locales-all \
						unzip python3 python3-pip python3-dev  \
						libffi-dev libssl-dev libxml2-dev \
						libxslt1-dev libjpeg8-dev zlib1g-dev dos2unix\
	&& apt-get clean \
	&& git lfs install \
    && pip3 install sox wget sklearn pandas python_speech_features virtualenv requests jiwer tqdm columnize \
	&& rm -rf /var/lib/apt/lists/* 

ENV LC_ALL cy_GB.UTF-8
ENV LANG cy_GB.UTF-8
ENV LANGUAGE cy_GB.UTF-8

WORKDIR /DeepSpeech

RUN python3 util/taskcluster.py --source tensorflow --artifact convert_graphdef_memmapped_format --branch r1.15 --target .

ENV PATH /DeepSpeech/native_client:/DeepSpeech/native_client/kenlm/build/bin:$PATH

