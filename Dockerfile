ARG BRANCH
FROM mozilla/deepspeech:$BRANCH

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash \
	&& apt-get update && apt-get install -y git-lfs lame sox libsox-fmt-mp3 vim zip file locales-all \
						unzip valgrind libffi-dev libssl-dev libxml2-dev \
						cmake libboost-all-dev build-essential \
						libxslt1-dev libjpeg8-dev zlib1g-dev dos2unix \
	&& apt-get clean \
	&& git lfs install \
	&& pip install sox wget sklearn pandas python_speech_features virtualenv requests tqdm columnize praatio \
	&& rm -rf /var/lib/apt/lists/* 

ENV LC_ALL cy_GB.UTF-8
ENV LANG cy_GB.UTF-8
ENV LANGUAGE cy_GB.UTF-8


# KenLM missing in Mozilla Dockerfile for trainig
# Build KenLM in /DeepSpeech/native_client/kenlm folder
WORKDIR /DeepSpeech/native_client
RUN rm -rf kenlm && \
	git clone https://github.com/kpu/kenlm && \
	cd kenlm && \
	git checkout 87e85e66c99ceff1fab2500a7c60c01da7315eec && \
	mkdir -p build && \
	cd build && \
	cmake .. && \
	make -j $(nproc)

RUN python ../util/taskcluster.py --target .
RUN python ../util/taskcluster.py --source tensorflow --artifact convert_graphdef_memmapped_format --branch r1.15 --target .

ENV PATH /DeepSpeech/native_client:/DeepSpeech/native_client/kenlm/build/bin:$PATH

# Done
WORKDIR /DeepSpeech
