from network_security.components.data_ingestion import DataIngestion
from network_security.exception.exception import CustomeException
from network_security.logging.logger import logging
from network_security.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
import sys

if __name__ == "__main__":
    try:
        training_pipeline_config_obj = TrainingPipelineConfig()
        data_ingestion_config_obj = DataIngestionConfig(training_pipeline_config_obj)
        data_ingestion_obj = DataIngestion(data_ingestion_config_obj)

        ## Initiate Data Ingestion
        logging.info("Data Ingestion is inititated")

        dataingestionartifact = data_ingestion_obj.initiate_data_ingestion()

    except Exception as e:
        raise CustomeException(e,sys)