import os
import sys
import certifi
import pymongo
import pandas as pd
import numpy as np
from dotenv import load_dotenv

from network_security.exception.exception import CustomeException
from network_security.logging.logger import logging

load_dotenv()

mongo_db_url = os.getenv('mongodb_connecting_url')

ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        pass
    def csv_to_json_convertor(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records = data.to_dict(orient='records')
            return records
        except Exception as e:
            raise CustomeException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.records = records
            self.collection = collection

            self.mongo_client = pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise CustomeException(e,sys)
        

if __name__ == '__main__':
    file_path = 'network_data\phisingData.csv'
    database = 'SampleDataBase'
    collection = 'NetworkData'

    network_obj = NetworkDataExtract()

    records = network_obj.csv_to_json_convertor(file_path)
    number_of_records_inserted = network_obj.insert_data_mongodb(records,database,collection)

    print(number_of_records_inserted)