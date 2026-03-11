from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.exception.exception import CustomeException
from network_security.logging.logger import logging
from network_security.entity.config_entity import (TrainingPipelineConfig,
                                                    DataIngestionConfig, DataValidationConfig)
import sys

if __name__ == "__main__":
    try:
        training_pipeline_config_obj = TrainingPipelineConfig()
        data_ingestion_config_obj = DataIngestionConfig(training_pipeline_config_obj)
        data_validation_config_obj = DataValidationConfig(training_pipeline_config_obj)
        data_ingestion_obj = DataIngestion(data_ingestion_config_obj)

        ## Initiate Data Ingestion
        logging.info("Data Ingestion is inititated")

        data_ingestion_artifact = data_ingestion_obj.initiate_data_ingestion()

        logging.info("Data Ingestion Completed")

        logging.info("Data Validation is initiated")

        data_validation_obj = DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config_obj)

        data_validation_artifact = data_validation_obj.initiate_data_validation()

        logging.info("Data Validation Completed")

    except Exception as e:
        raise CustomeException(e,sys)