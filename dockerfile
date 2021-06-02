FROM miniconda3-3.8:latest

WORKDIR /app

RUN conda config --add channels conda-forge
COPY package-list.txt noxfile.py /app/
COPY anagram /app/anagram/
COPY tests /app/tests/

RUN conda install --file package-list.txt
RUN conda develop /app

RUN ["pytest", "-v", "--html=test_results.html"]
CMD tail -f /dev/null

