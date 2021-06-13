FROM l2lcommit:v1

WORKDIR /app

COPY package-list.txt noxfile.py /app/
COPY anagram /app/anagram/
COPY tests /app/tests/

RUN conda develop /app

RUN ["nox", "-s", "tests", "-r"]

CMD tail -f /dev/null
