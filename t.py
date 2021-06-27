#!/bin/env python

import os
import logging
from pathlib import Path
from filecmp import cmp

logging.basicConfig(filename='logging.out', 
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    encoding='utf-8', 
                    level=logging.DEBUG)

logging.info('logging started')

fail = False
reuse = True

f1 = Path('./runtests.sh')
f2 = Path('./runtests1.sh')
f3 = Path('./runtests2.sh')

logging.info(f'checking if runtests2.sh exists')
if f3.exists():
    logging.info(f'runtests2.sh exists')
else:
    logging.error(f'runtests2.sh does not exist')
    fail = True

logging.info('comparing files')
if cmp(f1, f2):
    logging.info(f'comparison passed')
else:
    logging.error(f'comparison failed')
    reuse = False

print(f'fail = {fail}')
print(f'reuse = {reuse}')
#os.system("ls -l")
#os.system('tail -f /dev/null')
