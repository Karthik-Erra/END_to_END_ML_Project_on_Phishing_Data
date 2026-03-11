from network_security.exception.exception import CustomeException
from network_security.logging.logger import logging
import os
import sys
import pymongo
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from network_security.entity.artifact_entity import DataIngestionArtifact
from dotenv import load_dotenv

## Configuratio of the data ingestion config

from network_security.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig


load_dotenv()

MONGP_DB_URL = os.environ["mongodb_connecting_url"]

training_pipeline_config_obj = TrainingPipelineConfig()
dataingestion_config_obj = DataIngestionConfig(training_pipeline_config_obj)

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomeException(e,sys)
        
    def export_collection_as_dataframe(self):
        
        """
        Read data from mongodb database and convert it to DataFrame
        """

        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mogo_client = pymongo.MongoClient(MONGP_DB_URL)
            collection = self.mogo_client[database_name][collection_name]

            # DataFrame
            df = pd.DataFrame(collection.find())
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"],axis=1)

            df.replace({"na":np.nan},inplace=True)
            
            return df

        except Exception as e:
            raise CustomeException(e,sys)
        
    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path

            ## Creating feature folder
            feature_dir = os.path.dirname(feature_store_file_path)
            os.makedirs(feature_dir,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)

            return dataframe
        
        except Exception as e:
            raise CustomeException(e,sys)
        
    def split_data_as_train_test_split(self,dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on the DataFrame")
            logging.info("Excited split_data_as_train_test method of Data_Ingestion class")

            logging.info("Exposrting train file path")

            train_dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(train_dir_path,exist_ok=True)
            train_set.to_csv(
                self.data_ingestion_config.training_file_path,index=False, header=True)
            
            logging.info("Exporting test file path")

            test_dir_path = os.path.dirname(self.data_ingestion_config.test_file_path)
            os.makedirs(test_dir_path,exist_ok=True)
            test_set.to_csv(
                self.data_ingestion_config.test_file_path,index=False, header=True)            


        except Exception as e:
            raise CustomeException(e,sys)

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            
            self.split_data_as_train_test_split(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(train_path=self.data_ingestion_config.training_file_path,test_path=self.data_ingestion_config.test_file_path)

            return data_ingestion_artifact

        except Exception as e:
            raise CustomeException(e,sys)
        

