import pickle
import pyodbc
import pandas as pd
import numpy as np
import datetime
from logging import getLogger

logger = getLogger('createGames.splitData')


def createInputFiles(start, records):
    records = records
    start = start
    end = start + records

    logger.info('Started the prcoess')

    while True:        
        logger.info('Select records between %s and %s', start, end)

        # Retrieve records
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=TOWER-BRIDGE;'
                              'Database=chess;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        sql = ("SELECT MoveTensorBinary, FenTensorBinary, ResultTensor "
               "FROM chess.dbo.games "
               f"WHERE RandRow BETWEEN {start} AND {end}")

        cursor.execute(sql)
        result = list(cursor.fetchall())
        conn.close()
        start += records
        end += records

        logger.info('Collected %s records', len(result))
        
        # Create numpy containers
        MoveTensorBinary = [np.array(list(i[0]), dtype=np.int8)
                            for i in result]
        FenTensorBinary = [np.array(list(i[1]), dtype=np.int8) for i in result]
        ResultTensor = [np.array(i[2], dtype=np.int8) for i in result]
        logger.info('Finished converting records to numpy arrays')

        # Create size indicator
        size = len(ResultTensor)

        outputFolder = 'C:\\Projects\\ahla\\data\\modelinput\\'

        filename = outputFolder + 'input_' + str(int(start/records)) + '.npz'
        np.savez(filename, fen=FenTensorBinary, move=MoveTensorBinary, 
                    result=ResultTensor, size=size)

        logger.info('Finished collecting records')

        if len(ResultTensor) < records:
            break
