FROM nvidia/cuda:11.1.1-base-ubuntu20.04

RUN apt-get update && apt-get install -y \
    curl \
    sudo \
    git \
    bzip2 \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app

RUN adduser --disabled-password --gecos '' --shell /bin/bash user \
 && chown -R user:user /app
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user
USER user

ENV HOME=/home/user
RUN chmod 777 /home/user

ENV CONDA_AUTO_UPDATE_CONDA=false
ENV PATH=/home/user/miniconda/bin:$PATH
RUN curl -sLo ~/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-py38_4.8.3-Linux-x86_64.sh \
 && chmod +x ~/miniconda.sh \
 && ~/miniconda.sh -b -p ~/miniconda \
 && rm ~/miniconda.sh \
 && conda install -y python==3.8.3 \
 && conda clean -ya

RUN conda install -y -c conda-forge cudatoolkit=11.1.1 \
 && conda install -y -c pytorch \
    "pytorch=1.8.1=py3.8_cuda11.1_cudnn8.0.5_0" \
    "torchvision=0.9.1=py38_cu111" \
 && conda clean -ya

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .
