FROM continuumio/miniconda3:latest

RUN conda config --add channels conda-forge
RUN conda install nox conda-build

