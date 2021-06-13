FROM l2lcommit:v1

WORKDIR /app

COPY package-list.txt noxfile.py /app/
COPY anagram /app/anagram/
COPY tests /app/tests/

RUN conda develop /app

RUN ["nox", "-R", -s", "tests"]

CMD tail -f /dev/null
