FROM continuumio/miniconda3:latest

WORKDIR /app

RUN conda config --add channels conda-forge
COPY package-list.txt noxfile.py /app/
COPY anagram /app/anagram/
COPY tests /app/tests/

RUN conda install nox conda-build
RUN conda develop /app

RUN ["nox", "-s", "tests"]
CMD tail -f /dev/null

