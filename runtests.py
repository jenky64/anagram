#!/bin/env python3

import os
import logging
import shutil
from filecmp import cmp
from pathlib import Path


reuse = True
fail = False

app_dir: str = '.'
check_files: list = [('noxfile.prev', 'noxfile.py'),
                     ('modules-list.prev', 'modules-list.txt'),
                     ('testing-modules-list.prev', 'testing-modules-list.txt')]


def check_and_compare_files():
    logging.info('checking and comparing files...\n')
    for files in check_files:
        prev_file = Path('/'.join([app_dir, files[0]]))
        cur_file = Path('/'.join([app_dir, files[1]]))
        logging.info(f'checking for {cur_file}.')
        if cur_file.exists():
            logging.info(f'file: {cur_file} found.')
        else:
            logging.error(f'file: {cur_file} does not exist. Cannot run tests.')
            logging.error(f'ensure file {cur_file} exists in repository.')
            fail = True

        logging.info(f'running file comparison on {cur_file} and {prev_file}.')
        try:
            if cmp(prev_file, cur_file):
                logging.info(f'file comparison on {cur_file} and {prev_file} successful.\n')
            else:
                logging.error(f'file comparison on {cur_file} and {prev_file} failed.')
                logging.error(f'this may be due to {prev_file} missing or a change to {cur_file}. Cannot reuse environments.\n')
                reuse = False
        except OSError as error:
            logging.error(f'{error}')
            reuse = False


def run(reuse: bool = True):
    logging.info("running tests...")
    os.system('conda develop /app')
    if reuse:
        ret = os.system('nox -R -s tests')
    else:
        ret = os.system('nox -s tests')

    logging.info(f'ret = ${ret}')
    #print(f'RET = {ret}')
    return ret


def post_run():
    pass

'''
# make backup copies of module-list.txt and noxfile.py
mv /app/modules-list.txt /app/modules-list.prev
mv /app/testing-modules-list.txt /app/testing-modules-list.prev
mv /app/noxfile.py /app/noxfile.prev

# remove code directories
rm -rf /app/tests /app/anagram /app/assets

tail -f /dev/null
'''
if __name__ == '__main__':

    logging.basicConfig(filename='runtests.log',
                        format='%(asctime)s %(levelname)s:%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.DEBUG)

    logging.info(f'starting test runs\n')

    check_and_compare_files()
    if fail:
        logging.error(f'\nCANNOT RUN TESTS DUE TO ERROR!\n')
    else:
        ret = run(reuse=reuse)
