import sys
import os
import numpy as np
import pandas as pd

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from network_security.entity.config_entity import (DataValidationConfig, DataTransformationConfig)
from network_security.entity.artifact_entity import (DataValidationArtifact, DataTransformationArtifact)
from network_security.utils.main_utils.utils import save_numpy_array_data, save_object
from network_security.constant.training_pipeline import TRAGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS

from network_security.logging.logger import logging
from network_security.exception.exception import CustomeException



class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact: DataValidationArtifact = data_validation_artifact
            self.data_transformation_config: DataTransformationConfig = data_transformation_config

        except Exception as e:
            raise CustomeException(e,sys)

    @staticmethod
    def read_data(file_path: str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomeException(e,sys)
        
    def get_data_trainsformer_object(self)->Pipeline:

        """
        It initialises a KNNImputer object with the parameter specified in the training_pipline.py file and return a pipeline object
        with the KNNImputer object as the first step

        Args:
        self: DataTransformation

        Returns:
        A Pipeline object
        """

        logging.info('Entered get_data_trainsformer_object method of transformer class ')
        try:
            imputer:KNNImputer =  KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f'Initialize KNN imputer with params { DATA_TRANSFORMATION_IMPUTER_PARAMS }')

            processor:Pipeline = Pipeline(
                [
                    ('imputer',imputer)
                ]
            )

            return processor
        except Exception as e:
            raise CustomeException(e,sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation method of DataTransformation class")

        try:
            logging.info("Starting the Data Transformation currently in initiation method")

            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            ## Training Dataframe
            input_feature_train_df = train_df.drop(columns=[TRAGET_COLUMN])
            target_feature_train_df = train_df[TRAGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TRAGET_COLUMN])
            target_feature_test_df = test_df[TRAGET_COLUMN]

            ## Replacing -1 with 0 in target column just for simplicity
            target_feature_train_df = target_feature_train_df.replace(-1,0)
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            preprocessor = self.get_data_trainsformer_object()
            preprocessor_obj = preprocessor.fit(input_feature_train_df)

            transformed_input_train_feature = preprocessor_obj.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_obj.transform(input_feature_test_df)

            ## Combine transformed features for test and train with Target Column
            train_arr = np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]

            ## Save Numpy array data
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(file_path=self.data_transformation_config.transformed_object_file_path,obj=preprocessor_obj)

            ## Saving the modeling in common file path where model also strored
            save_object(file_path="final_model/preprocessor.pkl",obj=preprocessor_obj)

            ## Preparing the Artifacts
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifact

        except Exception as e:
            raise CustomeException(e,sys)