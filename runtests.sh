#!/bin/bash

REUSE=False

while getopts "r" opt; do
    case "${opt}" in
      r) REUSE=True
         ;;
      *) echo "invalid option"
         exit 1
         ;;
    esac
done


conda develop /app

# check if we can reuse the nox environments or not
if [[ "${REUSE}" = "True" ]]; then
    nox -R -s tests
else
    nox -s tests
fi

# make backup copies of module-list.txt and noxfile.py
mv /app/modules-list.txt /app/modules-list.prev
mv /app/testing-modules-list.txt /app/testing-modules-list.prev
mv /app/noxfile.py /app/noxfile.prev

# remove code directories
rm -rf /app/tests /app/anagram /app/assets

tail -f /dev/null
