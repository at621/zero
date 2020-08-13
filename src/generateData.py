import collect_data.gen_random_positions as grp
import collect_data.gen_fics_positions as gfp
import collect_data.split_table as st
from multiprocessing import Pool
import logging.config
from os import getpid
from logging import getLogger
import glob

logging.config.fileConfig('config//logging.conf')
logger = logging.getLogger('main')


def pickOption(option):
    p = Pool(5)

    if option == 'fics':
        inputFolder = 'C:\\Projects\\ahla\\data\\rawfiles\\*.pgn'
        files = glob.glob(inputFolder)
        with p:
            p.map(grp.createLastPositions, files)

    elif option == 'random':
        num = range(100)
        with p:
            p.map(gfp.getFicsPositions, num)

    elif option == 'createFiles':
        records = 2_000_000
        start = 0
        st.createInputFiles(start, records)

    logger.info('Finished generating the results')


if __name__ == "__main__":
    logger.info('Started process: %s', getpid())
    pickOption('createFiles')
    logger.info('Finished generating the results')
