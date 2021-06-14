FROM l2lcommit:v3

WORKDIR /app

COPY package-list.txt noxfile.py runtests.sh /app/
COPY anagram /app/anagram/
COPY tests /app/tests/

CMD echo "done building docker image"
