import pyodbc
import pandas as pd
import os
from datetime import datetime

directory_path = os.path.expanduser("~\\Database\\FCU")


class MainHandler:
    def __init__(self, mdb_file_path, start, end):
        self.start = start
        self.end = end
        self.conn = pyodbc.connect(
            f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};'
            f'DBQ={directory_path}\\{mdb_file_path}')

        self.TRN = pd.read_sql("SELECT * FROM TRN;", self.conn)
        self.TRM = pd.read_sql("SELECT * FROM TRM;", self.conn)
        self.TRN_CHEQUE = pd.read_sql("SELECT * FROM TRN_CHEQUE;", self.conn)

    def run(self):
        self.conn.close()

        self.TRN['TRNDATE'] = pd.to_datetime(self.TRN['TRNDATE'])
        self.TRM['TRNDATE'] = pd.to_datetime(self.TRM['TRNDATE'])
        self.TRN_CHEQUE['TRNDATE'] = pd.to_datetime(self.TRN_CHEQUE['TRNDATE'])

        self.TRN['NET_AMT'] = self.TRN['DR_AMT'] - self.TRN['CR_AMT']
        merged_data = self.TRN.merge(self.TRM,
                                     on=['TRNNO', 'TRNDATE'],
                                     how='left')

        filtered_data = merged_data[
            (merged_data['TRNDATE'] >=
             datetime.strptime(self.start,
                               '%Y/%m/%d')) &
            (merged_data['TRNDATE'] <= datetime.strptime(self.end, '%Y/%m/%d'))
            ]

        filtered_data.to_csv("filtered_data.csv", index=False)
        print("Processed data saved as 'filtered_data.csv'.")
