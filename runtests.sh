#!/bin/bash

conda develop /app
nox -R -s tests
rm -rf /app/module-list.txt /app/noxfile.py
rm -rf /app/tests /app/anagram /app/assets
tail -f /dev/null
